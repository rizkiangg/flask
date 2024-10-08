from flask_mysqldb import MySQL
from flask import Flask

def init_db(app: Flask):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'agung'
    app.config['MYSQL_PASSWORD'] = 'Da240219'
    app.config['MYSQL_DB'] = 'my_db'

    mysql = MySQL(app)
    return mysql