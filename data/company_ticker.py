from db_connection import get_db_connection
from djia_companies import DJIA_LIST
import os

def getConnection():
    db_connection = get_db_connection()
    return db_connection


## inserting data

try:

    db_connection = get_db_connection()
    cursor = db_connection.cursor()

    QUERY = " INSERT INTO company_ticker (ticker, company_name) values (%s , %s )"

    cursor.executemany(QUERY,DJIA_LIST)

    db_connection.commit()
    db_connection.close()
except Exception as e:
    print("Exception in populating company_ticker ",e)    

