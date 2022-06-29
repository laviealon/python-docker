import mysql.connector
import json
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, Docker!'


# @app.route('/widgets')
# def get_widgets():
#     mydb = mysql.connector.connect(
#         host="mysqldb",
#         user="root",
#         password="p@ssw0rd1",
#         database="inventory"
#     )
#     cursor = mydb.cursor()
#
#     cursor.execute("SELECT * FROM widgets")
#
#     row_headers = [x[0] for x in cursor.description]  # this will extract row headers
#
#     results = cursor.fetchall()
#     json_data = []
#     for result in results:
#         json_data.append(dict(zip(row_headers, result)))
#
#     cursor.close()
#
#     return json.dumps(json_data)


@app.route('/counter')
def increment():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="counter_inv"
    )
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM counters LIMIT 1")

    # row_headers = [x[0] for x in cursor.description]  # this will extract row headers

    results = str(cursor.fetchall()[0][1])
    # json_data = []
    # for result in results:
    #     json_data.append(dict(zip(row_headers, result)))

    cursor.close()

    # return json.dumps(json_data)
    return results


@app.route('/initdb')
def db_init():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1"
    )
    cursor = mydb.cursor()

    cursor.execute("DROP DATABASE IF EXISTS counter_inv")
    cursor.execute("CREATE DATABASE counter_inv")
    cursor.close()

    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="counter_inv"
    )
    cursor = mydb.cursor()

    cursor.execute("DROP TABLE IF EXISTS counters")
    cursor.execute("CREATE TABLE counters (id int, value int);")
    cursor.close()

    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="counter_inv"
    )
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO counters (value) VALUES (0);")
    mydb.commit()
    cursor.close()

    return 'init database'


if __name__ == "__main__":
    app.run(host='0.0.0.0')
