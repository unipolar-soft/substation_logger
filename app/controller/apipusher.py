import psutil
import requests
import logging
import json
from logging.config import dictConfig
from ..projutil.log_conf import DIC_LOGGING_CONFIG
from ..projutil import conf
from ..db.database import DB

dictConfig(DIC_LOGGING_CONFIG)
logger = logging.getLogger(conf.LOGGER_NAME)

class APIPusher(object):

    def __init__(self, db: DB) -> None:
        self.db = db
        self.dateformat = "%Y-%m-%d %H:%M:%S"
        self.updateAdapter()

    def updateAdapter(self):
        adapter = self.db.get_value_from_key(conf.KEY_API_ADAPTER)
        self.address = psutil.net_if_addrs()[adapter][1].address

    def session_for_src_addr(self) -> requests.Session:
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
                source_address=(self.address, 0),
            )

        return session

    def post_request(self, data):
        headers = {'content-type': 'application/json'}
        url =  "http://192.168.0.98:8080/interruptionlog/api/pushlog.php"
        session = self.session_for_src_addr()

        try:
            if data["power_on_time"] != None:
                data["power_on_time"]  = data["power_on_time"].strftime(self.dateformat)
            else:
                data["power_off_time"]  = data["power_off_time"].strftime(self.dateformat)

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