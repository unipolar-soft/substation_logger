from concurrent.futures import thread
from datetime import datetime
import imp
import psutil
import queue
from threading import Thread
import time
import requests
import json
import logging
import copy
from PySide6.QtCore import Signal, QObject, QTimer
from queue import Queue
from opcua import Client
from opcua import ua
from ..db.database import DB
from ..db.tables import KeyStore
from logging.config import dictConfig
from ..projutil.log_conf import DIC_LOGGING_CONFIG
from ..projutil.util import show_message
from ..projutil import conf
from .jsonlogger import write_json

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

url = None
prefix = None
tags = None
adapter = None

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
        "station": tag_identifier.split(".")[1],
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
    while tryout <= 5 and not interrupt_flag:
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

def session_for_src_addr(addr: str) -> requests.Session:
    """
    Create `Session` which will bind to the specified local address
    rather than auto-selecting it.
    """
    session = requests.Session()
    for prefix in ('http://', 'https://'):
        session.get_adapter(prefix).init_poolmanager(
            # those are default values from HTTPAdapter's constructor
            connections=requests.adapters.DEFAULT_POOLSIZE,
            maxsize=requests.adapters.DEFAULT_POOLSIZE,
            # This should be a tuple of (address, port). Port 0 means auto-selection.
            source_address=(addr, 0),
        )

    return session

def post_request(data):
    global adapter
    headers = {'content-type': 'application/json'}
    url =  "http://192.168.0.98:8080/interruptionlog/api/pushlog.php"
    if not adapter:
        logger.error("No adapter configured for API")
        return
    address = psutil.net_if_addrs()[adapter][1].address
    session = session_for_src_addr(address)

    try:
        if data["power_on_time"] != "":
            data["power_on_time"]  = data["power_on_time"].strftime(dateformat)
        else:
            data["power_off_time"]  = data["power_off_time"].strftime(dateformat)

    #enclose data in an array, the API expectiing an array
        response = session.post(url, data=json.dumps([data]), headers=headers)
        response = response.json()
        if response["Status"]:
            logger.info(f"API data updated for {data['feeder_no']}")
            return True
        else:
            return False
    except requests.RequestException as e:
        logger.error(e)
        return False

def get_time_data(breaker_status) :
    breaker_status = int(breaker_status)
    #feeder is ON
    if breaker_status:
        return {
            "power_on_time": datetime.now(),
            "power_off_time":None
        }

    else:
        return {
            "power_on_time": None,
            "power_off_time": datetime.now()
        }

def log_data_change(changed_status, station):
    feeder_status = {
        "feeder_no": changed_status["Feeder_No"],
        "interruption_type": int(changed_status["Feeder_TRIP_Status"]),
        "current":{
            "currentA":changed_status["Feeder_Relay_IA"],
            "currentB":changed_status["Feeder_Relay_IB"],
            "currentC":changed_status["Feeder_Relay_IC"]
            }
    }
    time_data = get_time_data(changed_status["Feeder_Breaker_Status"])
    feeder_status.update(time_data)
    logger.debug({
        station: feeder_status
    })
    return feeder_status

def update_API(station):
    logger.info(f"Requesting server values for {station}")
    status_server = bulkread_machine_tags(station)
    if not status_server:
        logger.warning(f"Server returned no value for {station}")
        return
    
    logger.info({
        station: status_server
    })

    if station not in latest_machine_stat:
        latest_machine_stat[station] = status_server
        return

    # check if the server sent values are same as previously stored value.
    if (
        latest_machine_stat[station] != status_server
    ):
        latest_machine_stat[station] = status_server
        return log_data_change(latest_machine_stat[station], station)
        # log_to_db(machine, latest_machine_stat[machineid])
        # return
    else:
        logger.info("Previous value persists")
        return None


# this class hosts function that listens for data change notification in tags
class SubHandler(QObject):
    dataChanged = Signal(dict)

    # def __init__(self, callback) -> None:
    #     self.callback = callback

    """
    Client to subscription. It will receive events from server
    """

    def datachange_notification(self, node, val, data):
        logger.info("Data change event fired")
        # tag_update_queue.put((node, val, data))
        # self.callback(node, val, data)
        res = extract(node, val, data)
        self.dataChanged.emit(res)

    def event_notification(self, event):
        logger.info("Python: New event", event)

def connect(caller):
    if (not url) or (url == ''):
        show_message(conf.MSG_URL_NOT_CONFIGURED)
        return
    retry = 5
    client = None
    while retry > 0 and not interrupt_flag :
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
    opcConnectionStateChanged = Signal(bool)
    feederTriped = Signal(dict)
    run_flag = True
    connected = False

    def __init__(self,db, parent=None) -> None:
        super().__init__(parent)
        self.db = db
        self.load_conf()

    def load_conf(self):
        global url, prefix, tags, adapter

        url = self.db.get_value_from_key(conf.KEY_URL)
        prefix = self.db.get_value_from_key(conf.KEY_LINK)
        tags = self.db.get_tags()
        adapter = self.db.get_value_from_key(conf.KEY_API_ADAPTER)
    
    def start_service(self):
        global url, prefix, tags, adapter
        
        url = self.db.get_value_from_key(conf.KEY_URL)
        if not url:
            return(False, "No OPC URL is configured")
        
        prefix = self.db.get_value_from_key(conf.KEY_LINK)
        if not prefix:
            return(False, "No Prefix is configured")
        
        value = self.db.get_substation_paths()
        if not value:
            return(False, "No Substation is Added")
        
        tags =  self.db.get_tags()
        if not tags:
            return(False, "No Tag is Added")
        
        monitored_tags = self.db.get_tags(monitored=True)
        if not monitored_tags:
            return(False, "No Monitored Tag is Added")
        
        adapter = self.db.get_value_from_key(conf.KEY_API_ADAPTER)
        if not adapter:
            return(False, "No adapter Selected")
        
        # self.opcthread = Thread(target=self.opc_runner, daemon=True)
        # self.opcthread.start()
        self.opc_runner()
        return (self.connected, "")
        # timer = QTimer(self)
        # timer.setInterval(10000)
        # timer.timeout.connect(self.opc_runner)
        # timer.start()

    def is_alive(self):
        try:
            l = self.client.get_endpoints()
            logger.info("client is alive")
            return True
        except Exception as error:
            logger.error(error)
            return False
    
    def opcCallback(self, tag_data):
        # tag_data = 
        # broadcast_data_change(tag_data,changed_machine_status)
        if tag_data["value"] is not None:
            station = tag_data["station"]
            tag = tag_data["name"]
            # this checks if the notifying tag value already has been updated.
            if (
                station in latest_machine_stat
                and tag_data["value"] == latest_machine_stat[station][tag]
            ):
                logger.info("Previous value persists")
            else:
                logger.info(f"{tag} of {station} has changed to {str(tag_data['value'])}")
                logger.info(f'a full data scan for {station} en route')
                data = update_API(station)
                if data:
                    self.feederTriped.emit(data)
        else:
            logger.info(f"Update skipped for {tag_data['name']}")
    
    def opc_subscribe(self):
        handler = SubHandler()
        sub = self.client.create_subscription(500, handler)
        handler.dataChanged.connect(self.opcCallback)
        stations = self.db.get_substation_paths()

        logger.info(f"Total {len(stations)} devices found.")
        monitored_tags = self.db.get_tags(monitored=True)


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
                    self.opcConnectionStateChanged.emit(False)
                    break
        self.db.close()
        return True

    def opc_runner(self):
        if self.is_alive():
            self.connected = True
            # emit signal to broadcast client connection
            self.opcConnectionStateChanged.emit(True)
            pass
        # opc has stopped working, restart opc
        else:
            self.connected = False
            # emit signal to broadcast client disconnection
            self.opcConnectionStateChanged.emit(False)
            self.client = connect("opc_start")
            if self.client:
                self.opcConnectionStateChanged.emit(True)
                self.opc_subscribe()
                self.connected = True

    def stop_service(self):
        if self.client:
            self.client.disconnect()
            self.opcConnectionStateChanged.emit(False)

if __name__=="__main__":
    opc = OpcuaClient()
    # dv = ua.DataValue(ua.Variant(0, ua.VariantType.Int16))
    # dv.ServerTimestamp = None
    # dv.SourceTimestamp = None
    # opc.write_values([get_node_path("Device1", "process_end")], [dv])
    # opc.read_value("Scada_Process_Start")