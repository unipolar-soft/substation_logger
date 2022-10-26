import logging
from logging.config import dictConfig
from ..projutil.log_conf import DIC_LOGGING_CONFIG
from ..projutil.conf import LOGGER_NAME
from ..projutil.util import show_message
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from PySide6.QtSql import QSqlDatabase
from .tables import create_tables, KeyStore, SubStation, Tags
from sqlalchemy import update
from datetime import datetime
from .db_config import DATABASE_CONNECTION_NAME, DATABASE_NAME


dictConfig(DIC_LOGGING_CONFIG)
logger = logging.getLogger(LOGGER_NAME)


class DB:
    db = None
    engine = create_engine(
        f"sqlite:///{DATABASE_NAME}", echo=True, future=True)

    def __init__(self):
        create_tables(engine=self.engine)
        self.session = Session(self.engine)
        self.initialize_qsql()

    def get_session(self):
        return self.session

    def initialize_qsql(self):
        self.db = QSqlDatabase.addDatabase(
            "QSQLITE", connectionName=DATABASE_CONNECTION_NAME)
        self.db.setDatabaseName(DATABASE_NAME)
        if self.db.open():
            print("Database opened in QT")
        # self.ready_tables()
    
    def add_substation(self, name, path):
        try:
            if path == "":
                logger.error("No path for substation Provided")
                return False
            station = SubStation(name = name, path=path)
            self.session.add(station)
            self.session.commit()
            return station
        except IntegrityError:
            self.session.rollback()
            show_message("A substation with this path already exists")
            return False
    
    def add_tag(self, name, path, is_monitored):
        try:
            if path == "":
                logger.error("No path for tag Provided")
                return False
            tag = Tags(name = name, path=path, isMonitored=is_monitored)
            self.session.add(tag)
            self.session.commit()
            return tag
        except IntegrityError:
            self.session.rollback()
            show_message("A Tag with this path already exists")
            return False
    
    def update_substation(self, name, path):
        stmt = (
            update(SubStation)
            .filter(SubStation.path == path)
            .values(name=name, path=path)
        )
        self.session.execute(stmt)
        self.session.commit()
    
    def insert_into_keystore(self, key, value):
        if value == "":
            return
        kv = KeyStore(key=key, value=value)
        self.session.add(kv)
        self.session.commit()
        return kv

    def get_value_from_key(self, key):
        key_value = (self.session.query(KeyStore)
                     .filter_by(key=key)
                     .first()
                     )
        if key_value:
            return key_value.value
        else:
            return ''
    
    def update_or_insert_keyValue(self, key, value):
        item = self.session.query(KeyStore).filter_by(key=key).first()

        if item:
            item.value = value
        else:
            item = KeyStore(key=key, value=value)
        self.session.add(item)
        self.session.commit()
    
    def get_tags(self, monitored=False):
        if monitored:
            tags = self.session.query(Tags).filter_by(isMonitored=monitored).all()
        else:
            tags = self.session.query(Tags).all()
        tag_paths = []
        for tag in tags:
            tag_paths.append(tag.path)
        return tag_paths
    
    def get_substation(self, name=None):
        subs = []
        if not name:
            subs = self.session.query(SubStation).all()
        return subs

    def get_substation_paths(self, name=None):
        subs = self.get_substation(name)

        sub_paths = []
        for sub in subs:
            sub_paths.append(sub.path)
        return sub_paths
        
    def close(self):
        self.session.close()


if __name__ == "__main__":
    db = DB()
