"""API webservice using the Flask web framework which increments a counter every time the relevant endpoint is
hit. Count is persisted in a MySQL database.

See README.md for info on how to spin up the docker container and initialize the database.

Copyright Alon Lavie (c) June 2022.
"""
import mysql.connector
from flask import Flask

app = Flask(__name__)


@app.route('/')
def app_run():
    """ Test localhost endpoint to ensure app has run successfully.
    """
    return 'app run successfully'


@app.route('/counter')
def increment():
    """ Connect to MySQL DB, increment counter, and fetch the newly updated value.
    """
    db = mysql.connector.connect(
        host="mysql",
        user="root",
        password="p@ssw0rd1",
        database="counter_inv",
        port=3306
    )
    cursor = db.cursor()
    cursor.execute("UPDATE counters SET value = value + 1")
    db.commit()
    cursor.execute("SELECT * FROM counters LIMIT 1")

    results = str(cursor.fetchall()[0][1])
    cursor.close()
    db.close()

    return results


@app.route('/initdb')
def db_init():
    """ Initialize MySQL DB with one counter set to value 0. To be called whenever the DB is to be
    initiated or reset.
    """
    db = mysql.connector.connect(
        host="mysql",
        user="root",
        password="p@ssw0rd1",
        port=3306
    )
    cursor = db.cursor()

    cursor.execute("DROP DATABASE IF EXISTS counter_inv")
    cursor.execute("CREATE DATABASE counter_inv")
    cursor.close()

    db = mysql.connector.connect(
        host="mysql",
        user="root",
        password="p@ssw0rd1",
        database="counter_inv"
    )
    cursor = db.cursor()

    cursor.execute("DROP TABLE IF EXISTS counters")
    cursor.execute("CREATE TABLE counters (id int, value int);")
    cursor.close()

    db = mysql.connector.connect(
        host="mysql",
        user="root",
        password="p@ssw0rd1",
        database="counter_inv"
    )
    cursor = db.cursor()
    cursor.execute("INSERT INTO counters (value) VALUES (0);")
    db.commit()
    cursor.close()
    db.close()

    return 'database initiated successfully'


if __name__ == "__main__":
    app.run(host='0.0.0.0')
