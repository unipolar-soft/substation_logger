import psutil
import requests
import logging
import json
from logging.config import dictConfig
from ..projutil.log_conf import DIC_LOGGING_CONFIG
from ..projutil import conf
from ..db.database import DB
from PySide6.QtCore import QSettings

dictConfig(DIC_LOGGING_CONFIG)
logger = logging.getLogger(conf.LOGGER_NAME)

class APIPusher(object):

    def __init__(self) -> None:
        self.dateformat = "%Y-%m-%d %H:%M:%S"

        self.settings = QSettings()

    def get_address(self):
        adapter = self.settings.value(conf.API_INTERFACE, "Ethernet")
        address = psutil.net_if_addrs()[adapter][1].address
        return address

    # find session for the adapater
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
                source_address=(self.get_address(), 0),
            )

        return session

    def post_request(self, data):
        headers = {'content-type': 'application/json'}
        url = self.settings.value(conf.API_URL)
        # url =  "http://192.168.0.98:8080/interruptionlog/api/pushlog.php"
        session = self.session_for_src_addr()
        response = None
        try:
            if data["power_on_time"] != None:
                data["power_on_time"]  = data["power_on_time"].strftime(self.dateformat)
            else:
                data["power_off_time"]  = data["power_off_time"].strftime(self.dateformat)

        #enclose data in an array, the API expectiing an array
            response = session.post(url, data=json.dumps([data]), headers=headers)
            logger.info(response.json())
            logger.info(f"API data updated for {data['feeder_no']}")
            response.close()
            return True
        except requests.RequestException as e:
            logger.error(e)
            return False