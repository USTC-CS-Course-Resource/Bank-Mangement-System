from flask import Flask
from flask import request
from flask_cors import CORS
from flask import jsonify

import bankdb
from bankdb import *
from utils.err import *
from utils import create_conn
from webui import preprocess
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from login import *
import traceback

logger = Logger.get_logger('web')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.errorhandler(Exception)
def handle_bad_request(e):
    logger.error(f'[{e.__class__}] {traceback.format_exc()}')
    return f'[{e.__class__.__name__}] {e}', 400


@app.errorhandler(LoginExpired)
def handle_bad_request(e):
    logger.error(f'[{e.__class__}] {e}')
    return f'LoginExpired', 400


@app.route('/customer/insert_customer', methods=['POST'])
def insert_customer():
    with create_conn() as conn:
        data = preprocess(request.get_json(silent=True))
        jwt_decode(data['token'])
        data.pop('token')
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            customer.insert_customer_with_contacts(cursor, **data)
        conn.commit()
    return "ok"


@app.route('/customer/search_customer', methods=['POST'])
def search_customer():
    with create_conn() as conn:
        data = preprocess(request.get_json(silent=True))
        jwt_decode(data['token'])
        data.pop('token')
        data = preprocess(data)
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            ret = customer.get_customer_with_contacts(cursor, **data)
    return jsonify(ret)


@app.route('/customer/remove_customer', methods=['POST'])
def remove_customer():
    with create_conn() as conn:
        data = preprocess(request.get_json(silent=True))
        jwt_decode(data['token'])
        data.pop('token')
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            customer.remove_customer_with_contacts(cursor, data['cus_id'])
        conn.commit()
    return "ok"


@app.route('/customer/update_customer', methods=['POST'])
def update_customer():
    with create_conn() as conn:
        data = preprocess(request.get_json(silent=True))
        jwt_decode(data['token'])
        data.pop('token')
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            customer.update_customer_with_contacts(cursor, **data)
        conn.commit()
    return "ok"


@app.route('/account/open_account', methods=['POST'])
def open_account():
    with create_conn() as conn:
        data = preprocess(request.get_json(silent=True))
        jwt_decode(data['token'])
        data.pop('token')
        data = preprocess(data)
        logger.info(f'post args: {data}')
        data['date'] = datetime.now()
        with conn.cursor() as cursor:
            account.open_account(cursor, **data)
        conn.commit()
    return "ok"


@app.route('/account/search_account', methods=['POST'])
def search_account():
    with create_conn() as conn:
        data = preprocess(request.get_json(silent=True))
        jwt_decode(data['token'])
        data.pop('token')
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


@app.route('/account/get_cus_count_summary', methods=['POST'])
def get_cus_count_summary():
    with create_conn() as conn:
        data = preprocess(request.get_json(silent=True))
        jwt_decode(data['token'])
        data.pop('token')
        with conn.cursor() as cursor:
            ret = account.get_cus_count_summary(cursor)
    return jsonify(ret)


@app.route('/account/get_account_summary', methods=['POST'])
def get_account_summary():
    ret = pd.DataFrame(columns=['bra_name', 'date', 'balance', 'cus_count'])
    with create_conn() as conn:
        data = preprocess(request.get_json(silent=True))
        jwt_decode(data['token'])
        data.pop('token')
        with conn.cursor() as cursor:
            begin = sql_str2datetime('2020-07-01 00:00:00')
            end = datetime.now()
            timedelta = relativedelta(months=+1)
            for i in range(13):
                date = begin + timedelta * i
                balance_summary = account.get_balance_summary(cursor, date)
                balance_summary = pd.DataFrame(balance_summary, columns=['bra_name', 'balance'])
                cus_count_summary = account.get_cus_count_summary(cursor, date)
                cus_count_summary = pd.DataFrame(cus_count_summary, columns=['bra_name', 'cus_count'])
                account_summary = balance_summary.merge(cus_count_summary, on='bra_name')
                account_summary['date'] = date.strftime('%Y-%m-%d')
                logger.info(f'account summary up to {date}:\n{account_summary}')
                ret = pd.concat([ret, account_summary])
    ret = ret.sort_values(by=['bra_name', 'date'])
    return jsonify(ret.to_dict('records'))


@app.route('/account/remove_have_account', methods=['POST'])
def remove_have_account():
    with create_conn() as conn:
        data = preprocess(request.get_json(silent=True))
        jwt_decode(data['token'])
        data.pop('token')
        data['date'] = datetime.now()
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            account.remove_have_account(cursor, **data)
        conn.commit()
    return "ok"


@app.route('/account/update_account', methods=['POST'])
def update_account():
    with create_conn() as conn:
        data = preprocess(request.get_json(silent=True))
        jwt_decode(data['token'])
        data.pop('token')
        data['date'] = datetime.now()
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            account.update_account(cursor, **data)
        conn.commit()
    return "ok"


@app.route('/loan/insert_loan', methods=['POST'])
def insert_loan():
    with create_conn() as conn: 
        data = preprocess(request.get_json(silent=True))
        jwt_decode(data['token'])
        data.pop('token')
        data['date'] = datetime.now()
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            loa_id = loan.insert_loan_with_relations(cursor, **data)
        conn.commit()
    return jsonify(loa_id)


@app.route('/loan/search_loan', methods=['POST'])
def search_loan():
    with create_conn() as conn:
        data = preprocess(request.get_json(silent=True))
        jwt_decode(data['token'])
        data.pop('token')
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            ret = loan.search_loan(cursor, **data)
        conn.commit()
    return jsonify(ret)


@app.route('/loan/get_pay_loa_records', methods=['POST'])
def get_pay_loa_records():
    with create_conn() as conn:
        data = preprocess(request.get_json(silent=True))
        jwt_decode(data['token'])
        data.pop('token')
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
        data = preprocess(request.get_json(silent=True))
        jwt_decode(data['token'])
        data.pop('token')
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            cus_ids = loan.get_customer_info(cursor, data.get('loa_id'))
    logger.info(cus_ids)
    return jsonify(cus_ids)


@app.route('/loan/pay_loan', methods=['POST'])
def pay_loan():
    with create_conn() as conn:
        data = preprocess(request.get_json(silent=True))
        jwt_decode(data['token'])
        data.pop('token')
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            loan.insert_pay_loan(cursor, data.get('loa_id'), data.get('loa_pay_amount'), datetime.now())
        conn.commit()
    return "ok"


@app.route('/loan/remove_loan', methods=['POST'])
def remove_loan():
    with create_conn() as conn:
        data = preprocess(request.get_json(silent=True))
        jwt_decode(data['token'])
        data.pop('token')
        logger.info(f'post args: {data}')
        with conn.cursor() as cursor:
            loan.remove_loan_with_relations(cursor, data.get('loa_id'))
        conn.commit()
    return "ok"


@app.route('/loan/get_loan_summary', methods=['POST'])
def get_loan_summary():
    with create_conn() as conn:
        data = preprocess(request.get_json(silent=True))
        jwt_decode(data['token'])
        data.pop('token')
        with conn.cursor() as cursor:
            ret_month = loan.get_loan_summary(cursor)
            ret_season = loan.convert_loan_summary(ret_month, time_cycle='season')
            ret_year = loan.convert_loan_summary(ret_month, time_cycle='year')
    return jsonify({'month': ret_month, 'season': ret_season, 'year': ret_year})


@app.route('/login', methods=['POST'])
def login():
    data = preprocess(request.get_json(silent=True))
    logger.info(f'get login info {data}')
    if 'token' in data:
        # 传来了 token, 尝试先验证 token
        payload = jwt_decode(data['token'])
        if payload['username'] in ['admin']:
            logger.info('token: ok')
            return jsonify({'status': 'ok'})
        else:
            logger.info('token: error')
            return jsonify({'status': 'error'})
    else:
        username_password_dict = {
            'admin': '123456'
        }
        if username_password_dict.get(data['username']) == data['password']:
            token = jwt_encode(data['username'])
            logger.info('username-password: match')
            return jsonify({'status': 'ok', 'username': data['username'], 'token': token})
        else:
            logger.info('username-password: not match')
            return jsonify({'status': 'password wrong'})


@app.route('/bankdb/clear', methods=['POST'])
def clear_bankdb():
    with create_conn() as conn:
        data = preprocess(request.get_json(silent=True))
        jwt_decode(data['token'])
        data.pop('token')
        with conn.cursor() as cursor:
            clear_table(cursor, bankdb.all_tables)
        conn.commit()
    return "ok"


@app.route('/bankdb/initialize', methods=['POST'])
def initialize_bankdb():
    with create_conn() as conn:
        data = preprocess(request.get_json(silent=True))
        jwt_decode(data['token'])
        data.pop('token')
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
