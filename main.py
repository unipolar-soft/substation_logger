# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication
from app.controller.mainwindow import MainWindow
from app.projutil.util import show_message
from app.db.utils import is_db_available


if __name__ == "__main__":
    app = QApplication([])
    if is_db_available(
        dbname="logger", 
        user="kb", 
        password="strongpass", 
        host="localhost", 
        port=5432
    ):
        widget = MainWindow()
        widget.show()
        sys.exit(app.exec())
    else:
        res = show_message("Database Connection Could not be made!")
        sys.exit(res)
    
