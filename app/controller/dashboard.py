# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import logging
from logging.config import dictConfig


from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QEvent,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter, QIntValidator, QDoubleValidator,
    QPalette, QPixmap, QRadialGradient, QTransform, QAction)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget, QMessageBox, QAbstractItemView,
    QMenu, QDialog, QDialogButtonBox, QVBoxLayout)

from ..ui.ui_dashboard import Ui_Dashboard
from ..projutil.log_conf import DIC_LOGGING_CONFIG
from ..projutil import conf
from ..projutil.util import show_message
from ..db.database import DB
from ..db.tables import FeederTrip
from ..models.tablemodel import TableModel
from ..res import icons
dictConfig(DIC_LOGGING_CONFIG)
logger = logging.getLogger(conf.LOGGER_NAME)

class DashBoard(QWidget):
    def __init__(self, db: DB):
        super(DashBoard, self).__init__()      
        self.db = db
        self.load_ui()

    def load_ui(self):
        self.ui = Ui_Dashboard()
        self.ui.setupUi(self)

        self.setupFeederTripTable()
        self.db.feederTripAdded.connect(self.feederTripRefresh)

    
    def feederTripRefresh(self):
        self.tripModel.select()

    def setupFeederTripTable(self):
        self.tripModel = TableModel(FeederTrip)
        self.ui.tripTableView.setModel(self.tripModel)
        self.ui.tripTableView.setCornerButtonEnabled(False)
        self.ui.tripTableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ui.tripTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tripTableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tripTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
    
    # def setIcons(self):
    #         icon = QIcon(QPixmap(":/icons/edit.png"))
    #         self.ui.urlEditBtn.setIcon(icon)
    #         self.ui.linkEditBtn.setIcon(icon)