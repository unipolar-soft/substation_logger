import logging
from opcua import Client
from ..projutil import conf
from logging.config import dictConfig
from ..projutil.log_conf import DIC_LOGGING_CONFIG
dictConfig(DIC_LOGGING_CONFIG)
logger = logging.getLogger(conf.LOGGER_NAME)

from ..db.database import DB

def testUrl(url):
    client = Client(url)
    try:
        client.connect()
        client.disconnect()
        return (True, "Connected")
    except Exception as e:
        logger.info(e)
        return (False, e)

def auditOPCConfig(db :DB):
    '''
    It checks for the presence of all required values for a successful opc connection.
    '''
    value = db.get_value_from_key(conf.KEY_URL)
    res = True
    msg = 'OPC is configuration is OK'
    if not value:
        msg = "No OPC URL is configured"
        res = False
    value = db.get_value_from_key(conf.KEY_LINK)
    if not value:
        msg = "No Channel is configured"
        res = False
    value = db.get_substation_paths()
    if not value:
        msg = "No Device is configured"
        res = False
    value =  db.get_tags()
    if not value:
        msg = "No Tag is configured"
        res = False
    return (res, msg)