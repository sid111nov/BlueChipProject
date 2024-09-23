import mysql.connector as mysql
from mysql.connector import Error
import os
import json

cwd = os.getcwd()
file_path = os.path.join(cwd, "config", "database.json")


def get_db_connection():

    try:


        with open(file_path, "r") as f:
            db_json = json.loads(f.read())

        dbconnection = mysql.connect(
            host=db_json["host"],
            user=db_json["username"],
            password=db_json["password"],
            database="finance",
        )

        return dbconnection
    except Error as e:
        print(e)


if __name__ == "__main__":
    db = get_db_connection()

    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    for x in cursor:
        print(x)
