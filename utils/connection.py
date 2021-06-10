import pymysql
from pymysql.connections import Connection


def create_conn():
    return Connection(host='localhost',
                      user='root',
                      password='',
                      database='bank',
                      charset='utf8mb4',
                      cursorclass=pymysql.cursors.DictCursor)
