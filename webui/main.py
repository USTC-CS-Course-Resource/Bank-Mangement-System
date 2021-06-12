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
    logger.error(f'[{e.__class__}] {e}')
    return f'[{e.__class__.__name__}] {e}', 400


@app.route('/customer/insert_customer', methods=['POST'])
def insert_customer():
    with create_conn() as conn:
        data = request.get_json(silent=True)
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            customer.insert_customer_with_contacts(cursor, **data)
        conn.commit()
    return "ok"


@app.route('/customer/search_customer', methods=['POST'])
def search_customer():
    with create_conn() as conn:
        data = request.get_json(silent=True)
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            ret = customer.get_customer_with_contacts(cursor, data['cus_id'])
    return jsonify(ret)


@app.route('/customer/remove_customer', methods=['POST'])
def remove_customer():
    with create_conn() as conn:
        data = request.get_json(silent=True)
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            customer.remove_customer_with_contacts(cursor, data['cus_id'])
        conn.commit()
    return "ok"


@app.route('/customer/update_customer', methods=['POST'])
def update_customer():
    with create_conn() as conn:
        data = request.get_json(silent=True)
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            customer.update_customer_with_contacts(cursor, **data)
        conn.commit()
    return "ok"


@app.route('/account/open_account', methods=['POST'])
def open_account():
    with create_conn() as conn:
        data = request.get_json(silent=True)
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            account.open_account(cursor, **data)
        conn.commit()
    return "ok"


@app.route('/account/search_account', methods=['POST'])
def search_account():
    with create_conn() as conn:
        data = request.get_json(silent=True)
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            store_ret = []
            check_ret = []
            if 'acc_type' in data:
                data['acc_type'] = account.AccountType.build(data['acc_type'])
                ret = account.get_account_info(cursor, **data)
                for i in range(len(ret)):
                    ret[i]['acc_type'] = account.AccountType.value_to_str(ret[i]['acc_type'])
                if data['acc_type'] == account.AccountType.STORE:
                    store_ret = ret
                elif data['acc_type'] == account.AccountType.CHECK:
                    check_ret = ret
                else:
                    raise UnknownAccountType
            else:
                store_ret = account.get_account_info(cursor, acc_type=account.AccountType(0), **data)
                check_ret = account.get_account_info(cursor, acc_type=account.AccountType(1), **data)
                for i in range(len(store_ret)):
                    store_ret[i]['acc_type'] = account.AccountType.value_to_str(store_ret[i]['acc_type'])
                for i in range(len(check_ret)):
                    check_ret[i]['acc_type'] = account.AccountType.value_to_str(check_ret[i]['acc_type'])
    print({'STORE': store_ret, 'CHECK': check_ret})
    logger.info({'STORE': store_ret, 'CHECK': check_ret})
    return jsonify({'STORE': store_ret, 'CHECK': check_ret})


@app.route('/account/remove_account', methods=['POST'])
def remove_account():
    with create_conn() as conn:
        data = request.get_json(silent=True)
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            account.remove_account(cursor, data.get('acc_id'))
        conn.commit()
    return "ok"


@app.route('/account/remove_have_account', methods=['POST'])
def remove_have_account():
    with create_conn() as conn:
        data = request.get_json(silent=True)
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            account.remove_have_account(cursor, **data)
        conn.commit()
    return "ok"


@app.route('/account/update_account', methods=['POST'])
def update_account():
    with create_conn() as conn:
        data = request.get_json(silent=True)
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            account.update_account(cursor, **data)
        conn.commit()
    return "ok"


@app.route('/loan/insert_loan', methods=['POST'])
def insert_loan():
    with create_conn() as conn:
        data = request.get_json(silent=True)
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            loa_id = loan.insert_loan_with_relations(cursor, **data)
        conn.commit()
    return jsonify(loa_id)


@app.route('/loan/search_loan', methods=['POST'])
def search_loan():
    with create_conn() as conn:
        data = request.get_json(silent=True)
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            ret = loan.search_loan(cursor, **data)
        conn.commit()
    return jsonify(ret)


@app.route('/loan/get_pay_loa_records', methods=['POST'])
def get_pay_loa_records():
    with create_conn() as conn:
        data = request.get_json(silent=True)
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            records = loan.get_pay_loa_records(cursor, data.get('loa_id'))
            loa_pay_amount_sum = loan.get_loa_pay_amount_sum(cursor, data.get('loa_id'))
    ret = {'payLoanRecords': records, 'loa_pay_amount_sum': loa_pay_amount_sum}
    logger.info(ret)
    return jsonify(ret)


@app.route('/loan/get_customer_info', methods=['POST'])
def get_customer_info():
    with create_conn() as conn:
        data = request.get_json(silent=True)
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            cus_ids = loan.get_customer_info(cursor, data.get('loa_id'))
    logger.info(cus_ids)
    return jsonify(cus_ids)


@app.route('/loan/pay_loan', methods=['POST'])
def pay_loan():
    with create_conn() as conn:
        data = request.get_json(silent=True)
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            loan.insert_pay_loan(cursor, data.get('loa_id'), data.get('loa_pay_amount'))
        conn.commit()
    return "ok"


@app.route('/loan/remove_loan', methods=['POST'])
def remove_loan():
    with create_conn() as conn:
        data = request.get_json(silent=True)
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            loan.remove_loan_with_relations(cursor, data.get('loa_id'))
        conn.commit()
    return "ok"


@app.route('/bankdb/clear', methods=['GET'])
def clear_bankdb():
    # TODO: add authentication
    with create_conn() as conn:
        with conn.cursor() as cursor:
            clear_table(cursor, ['pay_loan', 'loan_relation', 'loan', 'have_store_account', 'store_account', 'account',
                                 'branch', 'contacts', 'customer'])
        conn.commit()
    return "ok"


@app.route('/bankdb/initialize', methods=['GET'])
def initialize_bankdb():
    # TODO: add authentication
    with create_conn() as conn:
        with conn.cursor() as cursor:
            initialize(cursor)
        conn.commit()
    return "ok"


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
