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

        self.changed = False
        self.settings = QSettings()
        self.ui = Ui_DBConf()
        self.ui.setupUi(self)
        self.load_ui()
        self.ui.connectBtn.clicked.connect(self.dbConnect)

        self.ui.buttonBox.clicked.connect(self.cl)

        self.ui.hostEdit.editingFinished.connect(
            lambda : self.valueEdited(self.ui.hostEdit, conf.KEY_HOST)
            )
        self.ui.portEdit.editingFinished.connect(
            lambda : self.valueEdited(self.ui.portEdit, conf.KEY_PORT)
            )
        self.ui.userEdit.editingFinished.connect(
            lambda : self.valueEdited(self.ui.userEdit, conf.KEY_USER)
            )
        self.ui.passwordEdit.editingFinished.connect(
            lambda : self.valueEdited(self.ui.passwordEdit, conf.KEY_PASS)
            )
        self.ui.dbnameEdit.editingFinished.connect(
            lambda : self.valueEdited(self.ui.dbnameEdit, conf.KEY_DBNAME)
            )
    
    def valueEdited(self, editedUI, editedComponet):
        newVal = editedUI.text()
        prevValue = self.settings.value(editedComponet, None)
        if prevValue != newVal:
            print(f'{prevValue}--{newVal}')
            self.changed = True

    def load_ui(self):
        host = self.settings.value(conf.KEY_HOST, None)
        port = self.settings.value(conf.KEY_PORT, None)
        user = self.settings.value(conf.KEY_USER, None)
        password = self.settings.value(conf.KEY_PASS, None)
        db_name = self.settings.value(conf.KEY_DBNAME, None)

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
            conf.KEY_HOST: host,
            conf.KEY_PORT: port,
            conf.KEY_USER: user,
            conf.KEY_PASS: password,
            conf.KEY_DBNAME:  db_name
        }
    
    def saveConfig(self):
        if self.changed:
            confs = self.extractConfs()
            self.settings.setValue(conf.KEY_HOST, confs[conf.KEY_HOST])
            self.settings.setValue(conf.KEY_PORT, confs[conf.KEY_PORT])
            self.settings.setValue(conf.KEY_USER, confs[conf.KEY_USER])
            self.settings.setValue(conf.KEY_PASS, confs[conf.KEY_PASS])
            self.settings.setValue(conf.KEY_DBNAME, confs[conf.KEY_DBNAME])

            logger.info(f"Database Config written as follows {confs}")

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
                host = confs[conf.KEY_HOST], 
                port = confs[conf.KEY_PORT], 
                user = confs[conf.KEY_USER], 
                password = confs[conf.KEY_PASS], 
                dbname = confs[conf.KEY_DBNAME]
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

