from utils.err import *
from utils import sql_datetime_format
from pymysql.cursors import Cursor
from enum import Enum
from utils.logger import Logger
from typing import Union
from datetime import datetime

logger = Logger.get_logger('bankdb')


class AccountType(Enum):
    STORE = 0
    CHECK = 1

    @staticmethod
    def build(t):
        if type(t) == str:
            t = AccountType.str_to_value(t)
        return AccountType(t)

    @staticmethod
    def str_to_value(string: str):
        string = string.lower()
        if string == 'store':
            return 0
        elif string == 'check':
            return 1
        else:
            return -1

    @staticmethod
    def value_to_str(value: int):
        if value == 0:
            return 'STORE'
        elif value == 1:
            return 'CHECK'
        else:
            return "UNKNOWN_TYPE"


def get_acc_type(cursor: Cursor, acc_id: str):
    cursor.execute("select acc_type from account where acc_id = %s", (acc_id,))
    acc_type = cursor.fetchone()
    logger.info(cursor.mogrify("select acc_type from account where acc_id = %s", (acc_id,)))
    if not acc_type:
        raise AccountNotExists
    return AccountType(acc_type.get('acc_type'))


def insert_account(cursor, acc_type, acc_id, sto_interest_rate=0.02, sto_currency_type='CNY'):
    if acc_type == AccountType.STORE:
        query = """
            insert into store_account(acc_id, sto_interest_rate, sto_currency_type)
            values (%s, %s, %s);
        """
        logger.debug(cursor.mogrify(query, (acc_id, sto_interest_rate, sto_currency_type)))
        cursor.execute(query, (acc_id, sto_interest_rate, sto_currency_type))
    elif acc_type == AccountType.CHECK:
        query = """
            insert into check_account(acc_id, che_overdraft)
            values (%s, 0);
        """
        logger.debug(cursor.mogrify(query, (acc_id,)))
        cursor.execute(query, (acc_id,))
    else:
        raise UnknownAccountType
    logger.info(f'create account: {acc_id}')


def insert_have_account(cursor, acc_type, cus_id, bra_name, acc_id, date: Union[datetime, str]):
    if type(date) is datetime:
        date = date.strftime(sql_datetime_format)
    if acc_type == AccountType.STORE:
        query = """
            insert into have_store_account(cus_id, bra_name, acc_id, sto_last_visit_date)
            values (%(cus_id)s, %(bra_name)s, %(acc_id)s, %(date)s);
        """
    elif acc_type == AccountType.CHECK:
        query = """
            insert into have_check_account(cus_id, bra_name, acc_id, che_last_visit_date)
            values (%(cus_id)s, %(bra_name)s, %(acc_id)s, %(date)s);
        """
    else:
        raise UnknownAccountType
    logger.debug(query, {'cus_id': cus_id, 'bra_name': bra_name, 'acc_id': acc_id, 'date': date})
    cursor.execute(query, {'cus_id': cus_id, 'bra_name': bra_name, 'acc_id': acc_id, 'date': date})
    logger.info(f'create have_account: {cus_id} has {acc_id}')


def open_account(cursor: Cursor, date: Union[datetime, str],
                 acc_id: str, acc_type: Union[AccountType, int],
                 cus_id: str, bra_name: str, sto_interest_rate: float = None, sto_currency_type: str = 'CNY'):
    if type(date) is datetime:
        date = date.strftime(sql_datetime_format)
    if type(acc_type) == int:
        acc_type = AccountType(acc_type)
    # check is customer exists
    query = "select cus_id from customer where cus_id = %s;"
    logger.debug(cursor.mogrify(query, (cus_id,)))
    cursor.execute(query, (cus_id,))
    result = cursor.fetchone()
    logger.debug(result)
    if not result:
        raise CustomerNotFound
    # We don't need to check manually due to the primary key constraints.
    # Now insert data
    try:
        query = """
            insert into account (acc_id, acc_balance, acc_type, acc_open_date)
            values (%s, 0, %s, %s);
        """
        logger.debug(cursor.mogrify(query))
        cursor.execute(query, (acc_id, acc_type.value, date))
        insert_account(cursor, acc_type, acc_id, sto_interest_rate, sto_currency_type)
    except pymysql.err.IntegrityError:
        ...
    insert_have_account(cursor, acc_type, cus_id, bra_name, acc_id, date)
    update_account_log(cursor, acc_id=acc_id, cus_id=cus_id, log_type=1)
    update_account_update_log(cursor, acc_id=acc_id, log_date=date)
    update_last_visit_time(cursor, acc_id, cus_id, date)
    return acc_id


def get_account_info(cursor: Cursor, acc_type=None, acc_id: str = None, cus_id: str = None, bra_name: str = None):
    if not acc_type and not acc_id:
        raise ImplicitAccType
    # if given `acc_id` and not given `acc_type`, then use it to decide the `acc_type`
    if not acc_type and acc_id:
        try:
            acc_type = get_acc_type(cursor, acc_id)
        except AttributeError:
            # maybe no such an `acc_id`
            return []
    if acc_type == AccountType.STORE:
        query = """
            select hsa.cus_id as cus_id, acc.acc_id as acc_id, acc_balance, acc_type,
                sto_interest_rate as sto_interest_rate, sto_currency_type as sto_currency_type,
                bra_name as bra_name, sto_last_visit_date as sto_last_visit_date, acc_open_date
                from account as acc, store_account as sa, have_store_account as hsa
            where acc.acc_id = sa.acc_id and acc.acc_id = hsa.acc_id
        """
    elif acc_type == AccountType.CHECK:
        query = """
            select hca.cus_id, acc.acc_id as acc_id, acc_balance, acc_type,
                che_overdraft, bra_name , che_last_visit_date, acc_open_date
                from account as acc, check_account as ca, have_check_account as hca
            where acc.acc_id = ca.acc_id and acc.acc_id = hca.acc_id
        """
    else:
        raise UnknownAccountType
    if cus_id:
        query += cursor.mogrify(" and cus_id = %s", (cus_id,))
    if acc_id:
        query += cursor.mogrify(" and acc.acc_id = %s", (acc_id,))
    if bra_name:
        query += cursor.mogrify(" and bra_name = %s", (bra_name,))
    query += ';'
    cursor.execute(query)
    logger.debug(query)
    result = cursor.fetchall()
    logger.info(f'got account info: {result}')
    return result


def update_last_visit_time(cursor: Cursor, acc_id: str, cus_id: str, date: Union[datetime, str]):
    if not date:
        date = datetime.now()
    if type(date) is datetime:
        date = date.strftime(sql_datetime_format)
    acc_type = get_acc_type(cursor, acc_id)
    if acc_type == AccountType.STORE:
        query = """update have_store_account set sto_last_visit_date = %(date)s
                where cus_id = %(cus_id)s and acc_id = %(acc_id)s"""
        cursor.execute(query, {'cus_id': cus_id, 'acc_id': acc_id, 'date': date})
    elif acc_type == AccountType.CHECK:
        query = """update have_check_account set che_last_visit_date = %(date)s
                where cus_id = %(cus_id)s and acc_id = %(acc_id)s"""
        cursor.execute(query, {'cus_id': cus_id, 'acc_id': acc_id, 'date': date})
    logger.info(f'update last visited time for {cus_id} on {acc_id} to {date}')


def update_account(cursor: Cursor, acc_id: str, cus_id: str, date: Union[datetime, str], **kwargs):
    if type(date) is datetime:
        date = date.strftime(sql_datetime_format)
    acc_type = get_acc_type(cursor, acc_id)
    acc_keys = ['acc_balance']
    acc_kwargs = {k: v for (k, v) in kwargs.items() if k in acc_keys}
    logger.info(f'update {acc_kwargs} for {acc_id}')
    for k, v in acc_kwargs.items():
        cursor.execute(f"update account set {k} = %s where acc_id = %s;", (v, acc_id))
    if acc_type == AccountType.STORE:
        sto_keys = ['sto_interest_rate', 'sto_currency_type']
        sto_kwargs = {k: v for (k, v) in kwargs.items() if k in sto_keys}
        logger.info(f'update {sto_kwargs} for {acc_id}')
        for k, v in sto_kwargs.items():
            cursor.execute(f"update store_account set {k} = %s where acc_id = %s;", (v, acc_id))
    elif acc_type == AccountType.CHECK:
        che_keys = ['che_overdraft']
        che_kwargs = {k: v for (k, v) in kwargs.items() if k in che_keys}
        logger.info(f'update {che_kwargs} for {acc_id}')
        for k, v in che_kwargs.items():
            cursor.execute(f"update check_account set {k} = %s where acc_id = %s;", (v, acc_id))
    else:
        raise UnknownAccountType
    update_account_update_log(cursor, acc_id=acc_id, log_date=date)
    update_last_visit_time(cursor, acc_id, cus_id, date)


def get_balance(cursor: Cursor, acc_id: str):
    cursor.execute('select acc_balance from account where acc_id = %s', (acc_id,))
    return cursor.fetchone().get('acc_balance')


def get_overdraft(cursor: Cursor, acc_id: str):
    cursor.execute('select che_overdraft from check_account where acc_id = %s', (acc_id,))
    return cursor.fetchone().get('che_overdraft')


def remove_account(cursor: Cursor, acc_id: str, cascade=True):
    acc_type = get_acc_type(cursor, acc_id)
    acc_balance = get_balance(cursor, acc_id)
    if acc_balance != 0:
        raise StillHasBalance
    if cascade:
        if acc_type == AccountType.STORE:
            cursor.execute("delete from have_store_account where acc_id = %s;", (acc_id,))
            cursor.execute("delete from store_account where acc_id = %s;", (acc_id,))
        elif acc_type == AccountType.CHECK:
            che_overdraft = get_overdraft(cursor, acc_id)
            if che_overdraft != 0:
                raise StillHasOverdraft
            cursor.execute("delete from have_check_account where acc_id = %s;", (acc_id,))
            cursor.execute("delete from check_account where acc_id = %s;", (acc_id,))
        else:
            raise UnknownAccountType
    query = "delete from account where acc_id = %s;"
    cursor.execute(query, (acc_id,))
    logger.info(f'remove account {acc_id}')


def remove_have_account(cursor: Cursor, acc_id: str, cus_id: str, bra_name: str, date: Union[datetime, str], **_):
    if type(date) is datetime:
        date = date.strftime(sql_datetime_format)
    update_account_log(cursor, acc_id=acc_id, cus_id=cus_id, log_type=0, log_date=date)
    update_last_visit_time(cursor, acc_id, cus_id, date)
    acc_type = get_acc_type(cursor, acc_id)
    acc_balance = get_balance(cursor, acc_id)
    if acc_balance != 0:
        raise StillHasBalance
    if acc_type == AccountType.STORE:
        cursor.execute("delete from have_store_account where acc_id = %s and cus_id = %s and bra_name = %s;",
                       (acc_id, cus_id, bra_name))
    elif acc_type == AccountType.CHECK:
        che_overdraft = get_overdraft(cursor, acc_id)
        if che_overdraft != 0:
            raise StillHasOverdraft
        cursor.execute("delete from have_check_account where acc_id = %s and cus_id = %s and bra_name = %s;",
                       (acc_id, cus_id, bra_name))
    else:
        raise UnknownAccountType
    acc_info = get_account_info(cursor, acc_type, acc_id)
    logger.info(f'remove have account relation: {cus_id} has {acc_id}')
    logger.info(f'left relation: {acc_info}')
    if len(acc_info) == 0:
        remove_account(cursor, acc_id, cascade=True)


def update_account_update_log(cursor: Cursor, acc_id: str, log_date: Union[datetime, str], **kwargs):
    if type(log_date) is datetime:
        log_date = log_date.strftime(sql_datetime_format)
    data = get_account_info(cursor, acc_id=acc_id)
    data = data[0]
    data['log_date'] = log_date
    acc_type = AccountType.build(data['acc_type'])
    if acc_type == AccountType.STORE:
        query = """
            insert into 
            account_update_log (bra_name, acc_id, acc_balance, acc_type, 
                                sto_interest_rate, sto_currency_type, log_date)
            values (%(bra_name)s, %(acc_id)s, %(acc_balance)s, %(acc_type)s, %(sto_interest_rate)s,
                    %(sto_currency_type)s, %(log_date)s);
        """
        cursor.execute(query, data)
    elif acc_type == AccountType.CHECK:
        query = """
            insert into 
            account_update_log (bra_name, acc_id, acc_balance, acc_type, che_overdraft, log_date)
            values      (%(bra_name)s, %(acc_id)s, %(acc_balance)s, %(acc_type)s, %(che_overdraft)s, %(log_date)s);
        """
        cursor.execute(query, data)
    logger.info(f'inserted account update log for {acc_id}')


def update_account_log(cursor: Cursor, acc_id: str, cus_id: str, log_type: int, log_date: Union[datetime, str] = None):
    if type(log_date) is datetime:
        log_date = log_date.strftime(sql_datetime_format)
    data = get_account_info(cursor, acc_id=acc_id, cus_id=cus_id)
    data = data[0]
    data['log_type'] = log_type
    data['log_date'] = log_date or data['acc_open_date']
    query = """
        insert into 
        account_log (bra_name, acc_id, cus_id, acc_type, log_type, log_date)
        values      (%(bra_name)s, %(acc_id)s, %(cus_id)s, %(acc_type)s, %(log_type)s, %(log_date)s);
    """
    cursor.execute(query, data)
    logger.info(f'inserted account log: {data["cus_id"]} has {acc_id}')


def get_cus_count_summary(cursor: Cursor, date: Union[datetime, str] = None):
    if not date:
        date = datetime.now()
    if type(date) is datetime:
        date = date.strftime(sql_datetime_format)
    query = """
        select bra_name, count(*) as cus_count from account_log al
        where al.acc_type = 0 and al.log_type = 1 and al.log_date < %(date)s and al.cus_id not in (
              select distinct cus_id from account_log where acc_type = 0 and log_type = 0 and log_date < %(date)s
           )
        group by bra_name;
    """
    cursor.execute(query, {'date': date})
    cus_count_summary = cursor.fetchall()
    return cus_count_summary


def get_balance_summary(cursor: Cursor, date: Union[datetime, str] = None):
    if not date:
        date = datetime.now()
    if type(date) is datetime:
        date = date.strftime(sql_datetime_format)
    query = """
        select bra_name, sum(acc_balance) balance from account_update_log aul, 
           (
              select acc_id, max(log_date) as log_date, max(log_id) as log_id
              from account_update_log 
              where log_date < %(log_date)s
              group by acc_id
           ) max_date
        where aul.acc_type = 0 and aul.log_date = max_date.log_date 
            and aul.acc_id = max_date.acc_id and aul.log_id = max_date.log_id
        group by bra_name;
    """
    logger.debug(cursor.mogrify(query, {'log_date': date}))
    cursor.execute(query, {'log_date': date})
    balance_summary = cursor.fetchall()
    return balance_summary
