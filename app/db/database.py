import logging
from logging.config import dictConfig
from ..projutil.log_conf import DIC_LOGGING_CONFIG
from ..projutil import conf
from ..projutil.util import show_message
from sqlalchemy import create_engine, insert, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from PySide6.QtSql import QSqlDatabase
from PySide6.QtCore import QSettings
from .tables import create_tables, KeyStore, SubStation, Tags, FeederTrip
from sqlalchemy import update
from PySide6.QtCore import Signal, QObject
from .db_config import DATABASE_CONNECTION_NAME, DATABASE_NAME


dictConfig(DIC_LOGGING_CONFIG)
logger = logging.getLogger(conf.LOGGER_NAME)


class DB(QObject):
    # engine = create_engine(
    #     f"sqlite:///{DATABASE_NAME}", echo=True)
    engine = create_engine("postgresql+psycopg2://kb:strongpass@localhost:5432/logger")
    feederTripAdded = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # get database configs
        settings = QSettings()
        host = settings.value(conf.KEY_HOST)
        port = settings.value(conf.KEY_PORT)
        user = settings.value(conf.KEY_USER)
        password = settings.value(conf.KEY_PASS)
        db_name = settings.value(conf.KEY_DBNAME)

        self.engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}")

        create_tables(engine=self.engine)
        self.session = Session(self.engine)
        self.initialize_qsql(host, port, user, password, db_name)

    def initialize_qsql(self, host, port, user, password, db_name):
        if not QSqlDatabase.contains(DATABASE_CONNECTION_NAME):
            # db = QSqlDatabase.addDatabase(
            #     "QSQLITE", connectionName=DATABASE_CONNECTION_NAME)
            db = QSqlDatabase.addDatabase(
                "QPSQL", connectionName=DATABASE_CONNECTION_NAME)
            db.setDatabaseName(db_name)
            db.setHostName(host)
            db.setPort(int(port))
            db.setUserName(user)
            db.setPassword(password)
            if db.open():
                print("Database opened in QT")
            # self.ready_tables()
    
    def insert_into_keystore(self, key, value):
        with Session(self.engine) as session:
            if value == "":
                return
            kv = KeyStore(key=key, value=value)
            session.add(kv)
            session.commit()
            return kv

    def get_value_from_key(self, key):
        with Session(self.engine) as session:
            key_value = (session.query(KeyStore)
                        .filter_by(key=key)
                        .first()
                        )
            if key_value:
                return key_value.value
            else:
                return ''
    
    def update_or_insert_keyValue(self, key, value):
        with Session(self.engine) as session:
            item = session.query(KeyStore).filter_by(key=key).first()

            if item:
                item.value = value
            else:
                item = KeyStore(key=key, value=value)
            session.add(item)
            session.commit()
    
    def get_tags(self, monitored=False):
        with Session(self.engine) as session:
            if monitored:
                tags = session.query(Tags).filter_by(isMonitored=monitored).all()
            else:
                tags = session.query(Tags).all()
            tag_paths = []
            for tag in tags:
                tag_paths.append(tag.path)
            return tag_paths
    
    def add_tag(self, name, path, is_monitored):
        with Session(self.engine) as session:
            try:
                if path == "":
                    logger.error("No path for tag Provided")
                    return False
                tag = Tags(name = name, path=path, isMonitored=is_monitored)
                session.add(tag)
                session.commit()
                return tag
            except IntegrityError:
                session.rollback()
                show_message("A Tag with this path already exists")
                return False
    
    def add_substation(self, name, path, prefix):
        with Session(self.engine) as session:
            try:
                if path == "":
                    logger.error("No path for substation Provided")
                    return False
                station = SubStation(name = name, path=path, prefix=prefix)
                session.add(station)
                session.commit()
                return station
            except IntegrityError:
                session.rollback()
                show_message("A substation with this path already exists")
                return False
    
    def update_substation(self, name, path, prefix):
        with Session(self.engine) as session:
            stmt = (
                update(SubStation)
                .filter(SubStation.path == path, SubStation.prefix == prefix)
                .values(name=name, path=path, prefix=prefix)
            )
            session.execute(stmt)
            session.commit()
    
    def get_substation(self, name=None):
        subs = []
        with Session(self.engine) as session:
            if not name:
                subs = session.query(SubStation).all()
            else:
                subs = session.query(SubStation).filter_by(name=name).first()
        return subs
    
    def delete_substation(self,name:str, path:str, prefix:str):
        with Session(self.engine) as session:
            stmt = (
                delete(SubStation)
                .where(SubStation.path == path, SubStation.prefix == prefix)
                .execution_options(synchronize_session="fetch")
            )

            session.execute(stmt)
            session.commit()
    
    def delete_tag(self,name: str, path: str):
        with Session(self.engine) as session:
            stmt = (
                delete(Tags)
                .where(Tags.name == name)
                .execution_options(synchronize_session="fetch")
            )
            session.execute(stmt)
            session.commit()

    def get_substation_paths(self, name=None):
        subs = self.get_substation(name)

        sub_paths = []
        for sub in subs:
            sub_paths.append(sub.path)
        return sub_paths
    
    def add_feeder_trip(self, feeder_no, interruption_type, currentA, currentB,
                            currentC, power_on_time , power_off_time, api_updated=False):
        trip = FeederTrip(feeder_no = feeder_no, 
                   interruption_type = interruption_type, 
                   currentA = currentA, 
                   currentB = currentB,
                   currentC = currentC,
                   api_updated=api_updated)
        if power_on_time:
            trip.power_on_time = power_on_time
        else:
            trip.power_off_time = power_off_time
        with Session(self.engine) as session:
            session.add(trip)
            session.commit()
        self.feederTripAdded.emit()

        
    def close(self):
        self.session.close()


if __name__ == "__main__":
    db = DB()
