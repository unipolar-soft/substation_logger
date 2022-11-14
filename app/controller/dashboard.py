# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import logging
from logging.config import dictConfig


from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QEvent, QTimer,
    QSize, QTime, QUrl, Qt, QSortFilterProxyModel)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter, QIntValidator, QDoubleValidator,
    QPalette, QPixmap, QRadialGradient, QTransform, QAction)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget, QMessageBox, QAbstractItemView, QTableView,
    QMenu, QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout)

from PySide6.QtSql import QSqlDatabase

from ..ui.ui_dashboard import Ui_Dashboard
from ..projutil.log_conf import DIC_LOGGING_CONFIG
from ..projutil import conf
from ..projutil.util import show_message
from ..db.database import DB
from ..db.db_config import DATABASE_NAME
from ..db.tables import FeederTrip, SubStation
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
        # self.ui = QWidget(self)
        self.layout = QHBoxLayout()
        # self.setLayout(self.layout)

        self.setupFeederTripTable()
        self.db.feederTripAdded.connect(self.feederTripRefresh)

        self.setLayout(self.layout)

    
    def feederTripRefresh(self):
        self.tripModel.select()
        

    def setupFeederTripTable(self):
        self.tripModel = TableModel(FeederTrip, self)
        proxyModel = QSortFilterProxyModel(self)
        proxyModel.setSourceModel(self.tripModel)
        proxyModel.sort(0, Qt.DescendingOrder)
        
        tripTable = QTableView()
        self.layout.addWidget(tripTable)


        tripTable.setModel(proxyModel)
        tripTable.verticalHeader().setVisible(False)
        tripTable.setCornerButtonEnabled(False)
        tripTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        tripTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        tripTable.setSelectionMode(QAbstractItemView.SingleSelection)
        tripTable.setEditTriggers(QAbstractItemView.NoEditTriggers)