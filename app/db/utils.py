import psycopg2

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
