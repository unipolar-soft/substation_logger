import os
import json
import logging
from logging.config import dictConfig
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QSettings
from ..ui.ui_dbconf import Ui_DBConf
from ..db.utils import is_db_available

from ..projutil.log_conf import DIC_LOGGING_CONFIG
from ..projutil import conf

dictConfig(DIC_LOGGING_CONFIG)
logger = logging.getLogger(conf.LOGGER_NAME)
from pathlib import Path

class DBConf(QDialog):

    def __init__(self, parent= None):
        super().__init__(parent)

        self.ui = Ui_DBConf()
        self.ui.setupUi(self)
        self.load_ui()
        self.ui.connectBtn.clicked.connect(self.dbConnect)

        self.ui.buttonBox.clicked.connect(self.cl)
    
    def load_ui(self):
        settings =  QSettings()
        host = settings.value("host", None)
        port = settings.value("port", None)
        user = settings.value("user", None)
        password = settings.value("password", None)
        db_name = settings.value("db_name", None)

        self.ui.hostEdit.setText(host)
        self.ui.portEdit.setText(str(port))
        self.ui.userEdit.setText(user)
        self.ui.passwordEdit.setText(password)
        self.ui.dbnameEdit.setText(db_name)

    def extractConfs(self):
        host = self.ui.hostEdit.text()
        if host == "":
            self.show_error("No host provided")
            return None
        port = self.ui.portEdit.text()
        if port == "":
            self.show_error("No Port provided")
            return None
        port = int(port)
        user = self.ui.userEdit.text()
        if user == "":
            self.show_error("No user provided")
            return None
        password = self.ui.passwordEdit.text()
        if password == "":
            self.show_error("No password provided")
            return None
        db_name = self.ui.dbnameEdit.text()
        if db_name == "":
            self.show_error("No db name provided")
            return None
        return {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "db_name":  db_name
        }
    
    def saveConfig(self):
        confs = self.extractConfs()
        settings = QSettings()
        settings.setValue("host", confs["host"])
        settings.setValue("port", confs["port"])
        settings.setValue("user", confs["user"])
        settings.setValue("password", confs["password"])
        settings.setValue("db_name", confs["db_name"])

        logger.info("Database Config written as follows {confs}")

    def cl(self, btn):
        if btn.text() == "OK":
            self.saveConfig()
        else:
            print("Clicked")
        

    def show_error(self, msg):
        self.ui.con_msg.setStyleSheet("color:red")
        self.ui.con_msg.setText(msg)

    def dbConnect(self):
        confs = self.extractConfs()
        if confs:
            res, msg = is_db_available(
                host = confs["host"], 
                port = confs["port"], 
                user = confs["user"], 
                password = confs["password"], 
                dbname = confs["db_name"]
                )

            if res:
                self.ui.label_7.setStyleSheet("background:rgb(57, 240, 47)")
                self.ui.con_msg.setStyleSheet("")
                self.ui.con_msg.setText("Connected")
            else:
                msgs = msg.split(":")[-1]
                self.ui.con_msg.setText(msgs)
                self.ui.con_msg.setStyleSheet("color:red")
                self.ui.label_7.setStyleSheet("")

