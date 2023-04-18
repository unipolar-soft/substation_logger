# This Python file uses the following encoding: utf-8
import sys
import logging
import copy
from logging.config import dictConfig

from PySide6.QtWidgets import QMainWindow, QTabWidget, QInputDialog, QDialog
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import QSettings

from app.db.database import DB
from ..ui.ui_mainwindow import Ui_MainWindow
from ..controller.dbconfcontroller import DBConf
from ..controller.apipusherconfcontroller import APIPushConf
from ..controller.apipusher import APIPusher
from ..projutil.log_conf import DIC_LOGGING_CONFIG
from ..projutil import conf
from .opcwindow import OpcWindow
from .dashboard import DashBoard
from ..opc.opc import OpcuaClient

dictConfig(DIC_LOGGING_CONFIG)
logger = logging.getLogger(conf.LOGGER_NAME)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # member initializations
        self.db = DB()
        self.opcClient = OpcuaClient(self.db)
        self.settings = QSettings()
        self.apipusher = APIPusher()

        self.load_ui()
        adapter = self.db.get_value_from_key(conf.KEY_API_ADAPTER)
        if not adapter:
            self.db.update_or_insert_keyValue(conf.KEY_API_ADAPTER, "Ethernet")
        
        self.opcClient.feederTriped.connect(self.feederTripAdd)

    def dbReInitialize(self):
        self.db = DB()
        self.opcClient.db = self.db

    def feederTripAdd(self, feeder_status):
        logger.info(feeder_status)
        if feeder_status:
            api_push_enabled = self.settings.value(conf.API_PUSH_ENABLED, 0)
            if api_push_enabled:
                feeder_status_copy = copy.deepcopy(feeder_status)
                res = self.apipusher.post_request(feeder_status_copy)
                feeder_status["api_updated"] = res
            # feeder_status["api_updated"] = False
            # write_json(feeder_status)
            self.db.add_feeder_trip(
                feeder_no = feeder_status["feeder_no"],
                interruption_type = int(feeder_status["interruption_type"]), 
                currentA = feeder_status["current"]["currentA"], 
                currentB = feeder_status["current"]["currentB"],
                currentC = feeder_status["current"]["currentC"], 
                power_on_time = feeder_status["power_on_time"],
                power_off_time = feeder_status["power_off_time"],
                api_updated = feeder_status["api_updated"]
                )

    def load_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Dashboard")
        self.tabs = QTabWidget(self)
        self.tabs.addTab(DashBoard(self.db), "DashBoard")
        self.tabs.addTab(OpcWindow(self.db, self.opcClient), "OPC Conf")
        self.setCentralWidget(self.tabs)

        menuConnection = self.ui.menubar.addMenu("Connection")
        dbaction = menuConnection.addAction("Database")
        dbaction.triggered.connect(self.dbConfSelection)

        api_push_setting_action = menuConnection.addAction("API Settings")
        api_push_setting_action.triggered.connect(self.apiConfUpdate)

        self.opcClient.start_service()
    
    def apiConfUpdate(self):
        conf = APIPushConf()
        res = conf.exec()
    
    def dbConfSelection(self):
        conf = DBConf()
        conf.accepted.connect(self.dbReInitialize)
        res = conf.exec()
    
    # def closeEvent(self, event: QCloseEvent) -> None:
    #     self.opcClient.stop_service()
    #     print("Closing the window")
    #     return super().closeEvent(event)
    
    def cleanClose(self):
        self.opcClient.stop_service()
        sys.exit(0)