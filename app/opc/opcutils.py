import logging
from opcua import Client
from ..projutil import conf
from logging.config import dictConfig
from ..projutil.log_conf import DIC_LOGGING_CONFIG
dictConfig(DIC_LOGGING_CONFIG)
logger = logging.getLogger(conf.LOGGER_NAME)

def testUrl(url):
    client = Client(url)
    try:
        client.connect()
        root = client.get_root_node
        res = True if root else False
        client.disconnect()
        return res
    except Exception as e:
        logger.info(e)
        return False