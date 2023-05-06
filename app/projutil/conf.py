import os
import pathlib

APP_TITLE = "Substation Logger"
LOGGER_NAME = "sub_logger"
KEY_CHANNEL = "channel"
KEY_DEVICE = "device"
KEY_XTRAPATH = "extra_path"
KEY_LINK = "link"
KEY_URL = "url"
KEY_API_ADAPTER = "API_ADAPTER"

KEY_HOST = "host"
KEY_PORT = "port"
KEY_USER = "user"
KEY_PASS = "password"
KEY_DBNAME = "db_name"
KEY_DBMS = "dbms"

MSG_URL_NOT_CONFIGURED = "URL is not Configured"
MSG_Prefix_NOT_CONFIGURED = "Prefix is not Configured"

API_PUSH_ENABLED = "API_PUSH_ENABLED"
API_INTERFACE = "API_INTERFACE"
API_URL = "API_URL"
API_DATA_FORMAT = "API_DATA_FORMAT"

DBMS_PG = "pgsql"
DBMS_MS = "mssql"

"""takes the base directory of the project"""

# concat the base directory with the relative path of the file
FEEDER_IDS_FILE = os.path.expanduser("~\\Documents\\feeders.json")

# USER (36000000,ad45)
