from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from bankdb import *
import time
import os
import threading
from utils.logger import *
from utils.err import *
import pymysql
from pymysql.connections import Connection

logger = Logger.get_logger('web')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.errorhandler(Exception)
def handle_bad_request(e):
    return 'bad request!', 400


def create_conn():
    return Connection(host='localhost',
                      user='root',
                          password='',
                          database='bank',
                          charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)


@app.route('/customer/insert_customer', methods=['POST'])
def insert_customer():
    conn = create_conn()
    data = request.get_json(silent=True)
    logger.info(f'post args: {data}')
    # with cursor_with_exception_handler(conn) as cursor:
    with conn.cursor() as cursor:
        customer.insert_customer_with_contacts(cursor, **data)
    print(cursor)
    conn.commit()
    conn.close()
    return "ok"


if __name__ == '__main__':
    conn = create_conn()
    with cursor_with_exception_handler(conn) as cursor:
        clear_table(cursor, ['pay_loan', 'loan_relation', 'loan', 'have_store_account', 'store_account', 'account',
                             'branch', 'contacts', 'customer'])
    conn.close()
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
