import cx_Oracle
from config import Config

def get_db_connection():
    dsn = cx_Oracle.makedsn(Config.DB_HOST, Config.DB_PORT, service_name=Config.DB_SERVICE_NAME)
    conn = cx_Oracle.connect(user=Config.DB_USER, password=Config.DB_PASSWORD, dsn=dsn)
    return conn