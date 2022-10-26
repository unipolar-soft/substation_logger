import os
from threading import Thread
import time
import logging
from PySide6.QtCore import Signal, QObject
from queue import Queue
from opcua import Client
from opcua import ua
from ..db.database import DB
from ..db.tables import KeyStore
from logging.config import dictConfig
from ..projutil.log_conf import DIC_LOGGING_CONFIG
from ..projutil.util import show_message
from ..projutil import conf

dictConfig(DIC_LOGGING_CONFIG)
logger = logging.getLogger(conf.LOGGER_NAME)


# TODO
"""
   1. TimeoutError exception check at server read instances i.e. bulkread and execute
   2. Other Exceptions
"""
# this global flag is used to terminate running independent threads if 
# a SIGINT(CTRL+C) interruption is captured in main thread.
interrupt_flag = False

# a task queue to hold changed tags
tag_update_queue = Queue()

# store all latest machine status in dic to compare i runtime
latest_machine_stat = {}

# a global variable to pass the value of latest machine status
changed_machine_status = []

tags = KEPSERVER_CONF['tags']
monitored_tags = KEPSERVER_CONF['monitored_tags']
channel = KEPSERVER_CONF['channel']
devices = KEPSERVER_CONF['device']
extra_path = KEPSERVER_CONF['extra_path']
db = DB()
url = db.get_value_from_key(conf.KEY_URL)
prefix = db.get_value_from_key(conf.KEY_LINK)

dateformat = "%Y-%m-%d %H:%M:%S"
process_running = False
process_end_signal = None

def get_node_path(device: str, tag: str):
    if (not prefix) or (prefix == ""):
        show_message(conf.MSG_Prefix_NOT_CONFIGURED)
        return
    path = f"ns=2;s={prefix}.{device}.{tag}"
    # logger.info(path)
    return path

def extract(node, val, data):

    tag_identifier = node.nodeid.Identifier
    tag_name = tag_identifier[tag_identifier.rfind(".") + 1 :]
    tag_value = val

    data_value = data.monitored_item.Value
    tag_health = data.monitored_item.Value.StatusCode.name
    sourceT = data_value.SourceTimestamp
    serverT = data_value.ServerTimestamp
    tag_update_time = sourceT if sourceT else serverT
    tag_data = {
        "device": tag_identifier.split(".")[1],
        "name": tag_name,
        "path": tag_identifier,
        "value": tag_value,
        "health": tag_health,
        "last_updated": tag_update_time,
    }
    logger.debug(tag_data)
    return tag_data

def get_device_state(tag_data):
    global process_running
    # change this according to the PLC tag value
    if tag_data['value'] == 0 and not process_running:
        process_running = True
        return None
    elif tag_data['value'] == 1 and process_running:
        values = bulkread_machine_tags(tag_data['device'])
        process_running = False
        logger.info(values)
        return values
        

def bulkread_machine_tags(device):
    client = connect("bulkread")
    if not client:
        import os
        os.sys.exit(0)
        return None
    nodes = []
    for tag in tags:
        node_path = get_node_path(device, tag)
        node = client.get_node(node_path)
        nodes.append(node)
    # let's try at least five times before surrendering to server
    # anomalies. Server might not respond correctly at the first attempt,
    # in such a case we try four more times.
    tag_values = None
    tryout = 1
    while tryout <= 5:
        try:
            values = client.get_values(nodes)
            tryout = tryout + 1
            if values:
                tag_values = dict(zip(tags, values))
                """
                kepserver has provided with values, 
                so break out of tryout loop
                """
                break
        except Exception as e:
            logger.error(e)
    client.disconnect()

    if tag_values == len(tags)*[None]:
        logger.warning(f"Server returned no value for {device}")
        return None

    return tag_values
    
# this class hosts function that listens for data change notification in tags
class SubHandler(object):

    def __init__(self, callback) -> None:
        self.callback = callback
    """
    Client to subscription. It will receive events from server
    """

    def datachange_notification(self, node, value, data):
        logger.info("Data change event fired")
        tag_data = extract(node, value, data)
        if tag_data['health'] == 'Good':
            self.callback(tag_data)

    def status_change_notification(self, status):
        """
        called for every status change notification from server
        """
        logger.info(f'server status change notification {status}')

def connect(caller):
    if (not url) or (url == ''):
        show_message(conf.MSG_URL_NOT_CONFIGURED)
        return
    retry = 5
    client = None
    while retry > 0 :
        try:
            client = Client(url, timeout=10)
            client.connect()
            print("connected")
            return client
        except Exception as e:
            logger.error("OPC Connection can't be established")
            logger.error(e)
        retry -= 1
    return None

def signal_handler(signum, frame):
    logger.info(f"signal with {signum}")
    global interrupt_flag 
    interrupt_flag = True
    raise SystemExit   

class Tag():
    def __init__(self, tag_name, tag_data) -> None:
        self.name = tag_name
        self.data = tag_data
    
    def getName(self):
        return self.name
    
    def getData(self):
        return self.data
    
    def __str__(self) -> str:
        return f'tag: {self.name}, value:{self.data}'

class OpcuaClient(QObject):
    # process_end_signal = Signal(Batch)

    client = None

    
    def start_service(self):
        self.opcthread = Thread(target=self.opc_runner, daemon=True)
        self.opcthread.start()
    
    def processReportValues(self, tag_data):
        tag = tag_data['name']
        if tag == 'Report_Value_Aggr1':
            self.batch.aggr1 = tag_data['value']
        elif tag == "Report_Value_Aggr2":
            self.batch.aggr2 = tag_data['value']
        elif tag == 'Report_Value_Sand':
            self.batch.sand = tag_data['value']
        elif tag == 'Report_Value_Cement':
            self.batch.cement = tag_data['value']
        elif tag == 'Report_Value_Water':
            self.batch.water = tag_data['value']
        elif tag == 'Report_Value_Admixture':
            self.batch.admixture = tag_data['value']
        
        self.db.get_session().commit()
        
        self.process_end_signal.emit(self.batch)
    
    def processStatus(self, tag_data):
        tag = Tag(tag_data['name'], tag_data['value'])
        logger.info(f"Process Status Changed :: {tag}")

        self.processStatusChanged.emit(tag)
    
    def mixingValue(self, tag_data):
        tag = Tag(tag_data['name'], tag_data['value'])
        logger.info(f"Mixing value changed :: {tag}")
        self.mixingValueChanged.emit(tag)
    
    def actualValue(self, tag_data):
        tag = Tag(tag_data['name'], tag_data['value'])
        logger.info(f"Actual value changed :: {tag}")
        self.actualValueChanged.emit(tag)
    
    def dispValue(self, tag_data):
        tag = Tag(tag_data['name'], tag_data['value'])
        logger.info(f"Display value changed :: {tag}")
        self.dispValueChanged.emit(tag)
    
    def processStart(self, tag_data):
        tag = Tag(tag_data['name'], tag_data['value'])
        logger.info(f"Display value changed :: {tag}")
        self.processStartChanged.emit(tag)
    
    def processStop(self, tag_data):
        tag = Tag(tag_data['name'], tag_data['value'])
        logger.info(f"Display value changed :: {tag}")
        self.processStopChanged.emit(tag)

    def forOfValue(self, tag_data):
        tag = Tag(tag_data['name'], tag_data['value'])
        logger.info(f"For/Of value changed :: {tag}")
        self.forOfValueChange.emit(tag)

    def event_callback(self, tag_data):
        tag = tag_data['name']
        if tag.startswith("Report_Value"):
            self.processReportValues(tag_data)
        elif tag.endswith("_FB"):
            self.processStatus(tag_data)
        elif tag.startswith("Mixing_"):
            self.mixingValue(tag_data)
        elif tag.startswith("Actual_"):
            self.actualValue(tag_data)
        elif tag.startswith("Disp_"):
            self.dispValue(tag_data)
        elif tag.startswith("Scada_Process_Start"):
            self.processStart(tag_data)
        elif tag.startswith("Stop"):
            self.processStop(tag_data)
        elif tag.startswith("Of"):
            self.forOfValue(tag_data)
        elif tag.startswith("For"):
            self.forOfValue(tag_data)
    
    def writeSingleValue(self, value, variant, tag_name, device):
        dv = ua.DataValue(ua.Variant(value, variant))
        dv.ServerTimestamp = None
        dv.SourceTimestamp = None
        node = self.client.get_node(get_node_path(device, tag_name))
        return self.write_values([node],[dv])
   
    def write_values(self, nodes, values):
        try:
            if len(nodes) != len(values):
                logger.info("Number of tags don't correspond to number of values")
                return
            if not self.client:
                self.client = connect("write_value")
            self.client.set_values(nodes, values)
            logger.info("Value written to the ua server")
            return True
        except Exception as e:
            logger.error(e)
            return False

    def read_value(self, tag, device):
        if not self.client:
            self.client = connect("read")
        node = self.client.get_node(get_node_path(device, tag))

        vals = self.client.get_values([node])
        return vals[0]

    def is_alive(self):
        if not self.client:
            return None
        try:
            l = self.client.get_root_node()
            return True
        except Exception as error:
            logger.error(error)
            return False
    
    def opc_subscribe(self):
        sub = self.client.create_subscription(500, SubHandler(self.event_callback))

        stations = db.get_substation_paths()

        logger.info(f"Total {len(stations)} devices found.")
        monitored_tags = db.get_tags(monitored=True)


        for station in stations:
            for tag in monitored_tags:
                node_path = get_node_path(station, tag)
                logger.info(f"Trying to subscribe {node_path}")
                try:
                    sub.subscribe_data_change(self.client.get_node(node_path))
                    logger.info(f"subscribed to -> {node_path}")
                except Exception as e:
                    logger.error(e)
                    self.client.disconnect()
                    break
        return True

    def opc_runner(self):
        while 1:
            if self.is_alive():
                pass
                # opc has stopped working, restart opc
            else:
                self.client = connect("opc_start")
                if self.client:
                    self.opc_subscribe()
            time.sleep(3)

    def close_client(self):
        self.opcthread.join(1)
        self.client.disconnect()

if __name__=="__main__":
    opc = OpcuaClient()
    # dv = ua.DataValue(ua.Variant(0, ua.VariantType.Int16))
    # dv.ServerTimestamp = None
    # dv.SourceTimestamp = None
    # opc.write_values([get_node_path("Device1", "process_end")], [dv])
    # opc.read_value("Scada_Process_Start")