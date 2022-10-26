import queue
import signal
import time
from urllib import response
import requests
import json
from opcua import Client
from queue import Queue
from threading import Thread
from datetime import datetime


import logging
from jsonlogger import write_json
from logging_conf import DIC_LOGGING_CONFIG
from logging.config import dictConfig
from opc_server_conf import KEPSERVER_CONF, STATION_IP

dictConfig(DIC_LOGGING_CONFIG)
logger = logging.getLogger("dpdc.service")


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

tags = KEPSERVER_CONF['tag_names']
monitored_tags = KEPSERVER_CONF['monitored_tags']
channel = KEPSERVER_CONF['channel_name']
substations = KEPSERVER_CONF['device_names']

dateformat = "%Y-%m-%d %H:%M:%S"

def get_node_path(device, tag):
    return f"ns=2;s={channel}.{device}.{tag}"


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
        "station": tag_identifier.split(".")[-2],
        "name": tag_name,
        "path": tag_identifier,
        "value": tag_value,
        "health": tag_health,
        "last_updated": tag_update_time,
    }
    logger.debug(tag_data)
    return tag_data


def bulkread_machine_tags(station):
    client = connect("bulkread")
    if not client:
        import os
        os.sys.exit(0)
        return None
    nodes = []
    for tag in tags:
        node_path = get_node_path(station, tag)
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
        logger.warning(f"Server returned no value for {station}")
        return None

    return tag_values

def get_time_data(breaker_status) :
    time_now_str = datetime.now().strftime(dateformat)
    #feeder is ON
    if breaker_status:
        return {
            "power_on_time": time_now_str,
            "power_off_time":""
        }

    else:
        return {
            "power_on_time": "",
            "power_off_time": time_now_str
        }

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
    headers = {'content-type': 'application/json'}
    url =  "http://192.168.0.98:8080/interruptionlog/api/pushlog.php"

    session = session_for_src_addr(STATION_IP)

    try:
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

def broadcast_data_change(changed_status, station):

    feeder_status = {
        "feeder_no": changed_status["Feeder_No"],
        "interruption_type": int(changed_status["Feeder_TRIP_Status"]),
        "current":{
            "currentA":changed_status["Feeder_Relay_IA"],
            "currentB":changed_status["Feeder_Relay_IB"],
            "currentC":changed_status["Feeder_Relay_IC"]
            },
        "voltage": ""
    }
    time_data = get_time_data(changed_status["Feeder_Breaker_Status"])
    feeder_status.update(time_data)
    logger.info({
        station: feeder_status
    })
    res = post_request(feeder_status)
    feeder_status["api_updated"] = True if res else False
    write_json(feeder_status)

       
def update_API(station):
    logger.info(f"Requesting server values for {station}")
    status_server = bulkread_machine_tags(station)
    if not status_server:
        logger.warning(f"Server returned no value for {station}")
        return
    
    logger.info({
        station: status_server
    })

    # check if the server sent values are same as previously stored value.
    if (
        station not in latest_machine_stat
        or latest_machine_stat[station] != status_server
    ):
        latest_machine_stat[station] = status_server
        broadcast_data_change(latest_machine_stat[station], station)
        # log_to_db(machine, latest_machine_stat[machineid])
        return
    else:
        logger.info("Previous value persists")

def update():
    global interrupt_flag
    logger.info("Looking for event change data")
    while True:
        try:
            node, value, data = tag_update_queue.get(timeout=5)
            tag_data = extract(node, value, data)
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
                    update_API(station)
            else:
                logger.info(f"Update skipped for {tag_data['name']}")
            tag_update_queue.task_done()
        except queue.Empty:
            # the event queue is empty and an intruption by user is captured, 
            # so break out of the thread
            if interrupt_flag:
                break


# it is assumed that this funtion will be called from a different thread,
# other than the thread of the module itself. A new client is spwaned to avoid conflict
# with the Client of the module.
def all_scan(substations=None):
    if substations == None:
        substations = KEPSERVER_CONF['device_names']
    for station in substations:
        update_API(station)
    return True

# this class hosts function that listens for data change notification in tags
class SubHandler(object):

    """
    Client to subscription. It will receive events from server
    """

    def datachange_notification(self, node, val, data):
        logger.info("Data change event fired")
        tag_update_queue.put((node, val, data))

    def event_notification(self, event):
        logger.info("Python: New event", event)

def connect(caller):
    url = KEPSERVER_CONF['url']
    retry = 5
    client = None
    while retry > 0 :
        try:
            client = Client(url, timeout=10)
            client.connect()
            return client
        except Exception as e:
            logger.error("OPC Connection can't be established")
            logger.error(e)
        retry -= 1

def signal_handler(signum, frame):
    logger.info(f"signal with {signum}")
    global interrupt_flag 
    interrupt_flag = True
    raise SystemExit

if __name__ == "__main__":
    client = connect("Main")
    if not client:
        import os
        os.sys.exit(0)
    sub = client.create_subscription(500, SubHandler())

    logger.info(f"Total {len(substations)} substations found.")

    for station in substations:
        for tag in monitored_tags:
            node_path = get_node_path(station, tag)
            logger.info(f"subscribing to the node --> {node_path}")
            sub.subscribe_data_change(client.get_node(node_path))

    data_updater = Thread(target=update, daemon=False)

    try:
        data_updater.start()
        signal.signal(signal.SIGINT, signal_handler)
        while True:
            time.sleep(0.05)
    except SystemExit:
        data_updater.join()
        client.disconnect()
        logger.info("Exitting")