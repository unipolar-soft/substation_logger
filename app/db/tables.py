from .db_config import (
    TABLE_NAME_KEYSTORE, 
    TABLE_NAME_TAG, 
    TABLE_NAME_SUBSTATION,
    TABLE_NAME_FEEDERTRIP
    )
from sqlalchemy import Column
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy import Integer, Boolean, Float
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import inspect, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


Base = declarative_base()

class SubStation(Base):
    __tablename__ = TABLE_NAME_SUBSTATION
    name = Column(String, nullable=True, info={"verbose_name":"Name"})
    path = Column(String, primary_key=True, info={"verbose_name":"Server Path"})
    # prefix = Column("prefix", String(100), nullable=True)

class Tags(Base):
    __tablename__ = TABLE_NAME_TAG
    name = Column(String, nullable=True, info={"verbose_name":"Name"})
    path = Column(String, primary_key = True, info={"verbose_name":"Server Path"})
    isMonitored = Column(Boolean, default=False, info={"verbose_name":"Monitored"})

class FeederTrip(Base):
    __tablename__ = TABLE_NAME_FEEDERTRIP
    trip_id  = Column(Integer, primary_key=True, info={"verbose_name": "Trip ID"})
    feeder_no = Column(String, nullable=True, info={"verbose_name": "Feeder No"})
    interruption_type = Column(Integer, info={"verbose_name": "Interruption Type"})
    currentA = Column(Float, info={"verbose_name": "Current A"})
    currentB = Column(Float, info={"verbose_name": "Current B"})
    currentC = Column(Float, info={"verbose_name": "Current C"})
    power_on_time = Column(DateTime, nullable=True, info={"verbose_name": "On time"})
    power_off_time = Column(DateTime, nullable=True, info={"verbose_name": "Off time"})
    api_updated = Column(Boolean, info={"verbose_name": "API"})

class KeyStore(Base):
    __tablename__ = TABLE_NAME_KEYSTORE
    key = Column(String, primary_key=True)
    value = Column(String)

def create_tables(engine):
    Base.metadata.create_all(engine)
    update_tables(engine)

def check_if_column_exists(engine, table, column_name):
    inspector = inspect(engine)
    columns = inspector.get_columns(table)
    column_names = [c['name'] for c in columns]
    return column_name in column_names

def add_column(engine, table_name, column):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    is_nullable = 'NULL' if column.nullable else 'NOT NULL'
    with engine.connect() as conn:
        sql_statement = f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {column_name} {column_type} {is_nullable};"
        conn.execute(text(sql_statement))

  
def update_tables(engine):
    # add new columns to existing tables
    # add prefix column to substation table
    if not check_if_column_exists(engine, TABLE_NAME_SUBSTATION, "prefix"):
       column = Column("prefix", String(100), nullable=True)
       add_column(engine, TABLE_NAME_SUBSTATION, column)


if __name__ == "__main__":
    create_tables()

    # d = [column.info.get('verbose_name')
    #      for column in Formulation.__table__.columns]
    # print(d)
