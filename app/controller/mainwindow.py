# This Python file uses the following encoding: utf-8
from tkinter import dialog
import psutil
import logging
import copy
from logging.config import dictConfig

from PySide6.QtWidgets import QMainWindow, QTabWidget, QInputDialog
from PySide6.QtGui import QCloseEvent

from app.db.database import DB
from ..ui.ui_mainwindow import Ui_MainWindow
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

        self.load_ui()
        adapter = self.db.get_value_from_key(conf.KEY_API_ADAPTER)
        if not adapter:
            self.db.update_or_insert_keyValue(conf.KEY_API_ADAPTER, "Ethernet")
        
        self.opcClient.feederTriped.connect(self.feederTripAdd)
    
    def feederTripAdd(self, feeder_status):
        logger.debug(feeder_status)
        if feeder_status:
            feeder_status_copy = copy.deepcopy(feeder_status)
            # res = post_request(feeder_status_copy)
            # feeder_status["api_updated"] = True if res else False
            feeder_status["api_updated"] = False
            # write_json(feeder_status)
            self.db.add_feeder_trip(
                feeder_no = feeder_status["feeder_no"],
                interruption_type = int(feeder_status["interruption_type"]), 
                currentA = feeder_status["current"]["currentA"], 
                currentB = feeder_status["current"]["currentB"],
                currentC = feeder_status["current"]["currentC"], 
                power_on_time = feeder_status["power_on_time"],
                power_off_time = feeder_status["power_off_time"],
                api_updated = False
                )

    def load_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.tabs = QTabWidget(self)
        self.tabs.addTab(OpcWindow(self.db, self.opcClient), "OPC Conf")
        self.tabs.addTab(DashBoard(self.db), "DashBoard")
        self.setCentralWidget(self.tabs)

        menuConnection = self.ui.menubar.addMenu("Connection")
        action = menuConnection.addAction("API Adapter")
        action.triggered.connect(self.netInterfaceSelection)

        self.opcClient.start_service()
    
    def netInterfaceSelection(self):
        prev_adap = self.db.get_value_from_key(conf.KEY_API_ADAPTER)
        index = 0
        interfaces = psutil.net_if_addrs()
        interface_name_list = list(interfaces.keys())
        try:
            index = interface_name_list.index(prev_adap)
        except ValueError:
            logger.info("Previousl Selected Adapter Not Found")
        item, ok = QInputDialog.getItem(self, "Select API Interface",
                                "Interface", interface_name_list, index, False )
        if ok and item:
            self.db.update_or_insert_keyValue(conf.KEY_API_ADAPTER, item)
            logger.info(f"API Adapter Changed to {item}")
    
    def closeEvent(self, event: QCloseEvent) -> None:
        self.opcClient.close_client()
        print("Closing the window")
        # return super().closeEvent(event)
