import psycopg2
from PySide6.QtCore import QSettings
from ..projutil import conf

def getDBConf():
        '''
        checks if application configaration file already contains 
        a db connection parameters
        '''
        # filepath = "./app/db/db_con.json"
        # if os.path.isfile(filepath):
        #     with open(filepath) as f:
        #         js = json.load(f)
        #         return js
        # else:
        #     return False
        settings =  QSettings()
        host = settings.value(conf.KEY_HOST, None)
        port = settings.value(conf.KEY_PORT, None)
        user = settings.value(conf.KEY_USER, None)
        password = settings.value(conf.KEY_PASS, None)
        db_name = settings.value(conf.KEY_DBNAME, None)

        if host and port and user and password and db_name:
            return {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "db_name":  db_name
        }
        else:
            return False

def is_db_available(dbname, user, password, host="localhost", port=5432):
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

        conn.close()
        return (True, "Connected")

    except Exception as e:
        print(e)
        return (False, str(e))

if __name__ == "__main__":
    print("Check if there is a connection to postgres available")
    print(is_db_available(
        dbname="logger", 
        user="kb", 
        password="strongpass", 
        host="localhost", 
        port=5432
    ))
