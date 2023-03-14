import time
import psutil
import re
import logging
from logging.config import dictConfig
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QSettings
from ..ui.ui_api_settings import Ui_APIConfDialog

from ..projutil.log_conf import DIC_LOGGING_CONFIG
from ..projutil import conf

dictConfig(DIC_LOGGING_CONFIG)
logger = logging.getLogger(conf.LOGGER_NAME)

class APIPushConf(QDialog):

    def __init__(self, parent= None):
        super().__init__(parent)

        self.changed = False
        self.settings = QSettings()
        self.ui = Ui_APIConfDialog()
        self.ui.setupUi(self)
        self.load_ui()
        
        self.ui.update_pushButton.clicked.connect(self.update)
        self.ui.api_checkBox.clicked.connect(
            lambda : self.toggel_settings_availability(self.ui.api_checkBox.isChecked())
            )
        

    def update(self):

        if self.ui.api_checkBox.isChecked():
            res, msg = self.validateSettings()
            if not res:
                self.show_msg(msg=msg, success=False)
                return
            else:
                self._write_settings(
                    True,
                    self.ui.network_interface_Combobox.currentText(),
                    self.ui.api_url_lineEdit.text(),
                    self.ui.data_format_Combobox.currentText()
                    )
                self.show_msg(msg="API Settings Updated", success = True)

        else:
            self._write_settings(is_push=False)
            self.show_msg(msg="API Settings Updated", success = True)
        # update is successful, so close the dialog after waiting 2 seconds
        self.accept()

    def validateSettings(self):

        if self.ui.network_interface_Combobox.currentIndex()<0:
            return (False, "Network Interface Not Selected")
        
        _api_url = self.ui.api_url_lineEdit.text()
        url_pattern = re.compile(r"^(http|https|ftp)://([\w\-]+\.)+[\w\-]+(:\d+)?(/[^\s]*)?$")
        if not url_pattern.match(_api_url):
            return (False, "URL Format Not Valid")
        
        if self.ui.data_format_Combobox.currentIndex()<0:
            return (False, "No Data Format Not Selected")

        return (True, "Valid") 

    def _write_settings(self, is_push: bool, interface=None, url=None, data_format=None):
        self.settings.setValue(conf.API_PUSH_ENABLED, int(is_push))
        if interface and url and data_format:
            self.settings.setValue(conf.API_INTERFACE, interface)
            self.settings.setValue(conf.API_URL, url)
            self.settings.setValue(conf.API_DATA_FORMAT, data_format)

    def load_ui(self):

        _api_push_enabled = self.settings.value(conf.API_PUSH_ENABLED, 0)
        _api_push_enabled = bool(_api_push_enabled)
        _interface = self.settings.value(conf.API_INTERFACE, '')
        _url = self.settings.value(conf.API_URL, '')
        _data_format = self.settings.value(conf.API_DATA_FORMAT, '')

        self.ui.network_interface_Combobox.addItems(self.get_available_interface_list())
        self.ui.data_format_Combobox.addItems(['Array', 'Object'])

        self.ui.api_checkBox.setChecked(_api_push_enabled)
        self.ui.network_interface_Combobox.setCurrentText(_interface)
        self.ui.api_url_lineEdit.setText(_url)
        self.ui.data_format_Combobox.setCurrentText(_data_format)

        if not _api_push_enabled:
            self.toggel_settings_availability(enable=False)
    
    def toggel_settings_availability(self, enable):
        uis = [self.ui.network_interface_Combobox,
                self.ui.api_url_lineEdit,
                self.ui.data_format_Combobox
            ]
        for ui in uis:
            ui.setEnabled(enable)

    def get_available_interface_list(self):
        interfaces = psutil.net_if_addrs()
        interface_name_list = list(interfaces.keys())

        return interface_name_list

    def show_msg(self, msg, success=False):
        if not success:
            self.ui.update_message_level.setStyleSheet("color:red")
        else:
            self.ui.update_message_level.setStyleSheet("")
        self.ui.update_message_level.setText(msg)