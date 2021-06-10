from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from flask import jsonify
from bankdb import *
import time
import os
import threading
from utils.logger import *
from utils.err import *
from utils import create_conn

logger = Logger.get_logger('web')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.errorhandler(Exception)
def handle_bad_request(e):
    logger.error(e)
    return 'bad request!', 400


@app.route('/customer/insert_customer', methods=['POST'])
def insert_customer():
    with create_conn() as conn:
        data = request.get_json(silent=True)
        logger.info(f'post args: {data}')
        # with cursor_with_exception_handler(conn) as cursor:
        with conn.cursor() as cursor:
            customer.insert_customer_with_contacts(cursor, **data)
        conn.commit()
    return "ok"


@app.route('/customer/search_customer', methods=['POST'])
def search_customer():
    with create_conn() as conn:
        data = request.get_json(silent=True)
        logger.info(f'post args: {data}')
        # with cursor_with_exception_handler(conn) as cursor:
        with conn.cursor() as cursor:
            ret = customer.get_customer_with_contacts(cursor, data['cus_id'])
    return jsonify(ret)


@app.route('/customer/remove_customer', methods=['POST'])
def remove_customer():
    with create_conn() as conn:
        data = request.get_json(silent=True)
        logger.info(f'post args: {data}')
        # with cursor_with_exception_handler(conn) as cursor:
        with conn.cursor() as cursor:
            customer.remove_customer_with_contacts(cursor, data['cus_id'])
        conn.commit()
    return 'ok'


@app.route('/bankdb/clear', methods=['GET'])
def clear_bankdb():
    # TODO: add authentication
    with create_conn() as conn:
        with conn.cursor() as cursor:
            clear_table(cursor, ['pay_loan', 'loan_relation', 'loan', 'have_store_account', 'store_account', 'account',
                                 'branch', 'contacts', 'customer'])
        conn.commit()
    return "ok"


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
