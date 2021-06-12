from utils.err import *
from pymysql.cursors import Cursor
from enum import Enum
from utils.logger import Logger
from typing import Union

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
    return AccountType(cursor.fetchone().get('acc_type'))


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
        logger.debug(cursor.mogrify(query, (acc_id, )))
        cursor.execute(query, (acc_id, ))
    else:
        raise UnknownAccountType


def insert_have_account(cursor, acc_type, cus_id, bra_name, acc_id):
    if acc_type == AccountType.STORE:
        query = """
            insert into have_store_account(cus_id, bra_name, acc_id, sto_last_visit_date)
            values (%(cus_id)s, %(bra_name)s, %(acc_id)s, now());
        """
    elif acc_type == AccountType.CHECK:
        query = """
            insert into have_check_account(cus_id, bra_name, acc_id, che_last_visit_date)
            values (%(cus_id)s, %(bra_name)s, %(acc_id)s, now());
        """
    else:
        raise UnknownAccountType
    logger.debug(query, {'cus_id': cus_id, 'bra_name': bra_name, 'acc_id': acc_id})
    cursor.execute(query, {'cus_id': cus_id, 'bra_name': bra_name, 'acc_id': acc_id})


def open_account(cursor: Cursor,
                 acc_id: str, acc_type: Union[AccountType, int],
                 cus_id: str, bra_name: str, sto_interest_rate: float = None, sto_currency_type: str = 'CNY'):
    if type(acc_type) == int:
        acc_type = AccountType(acc_type)
    # check is customer exists
    query = "select cus_id from customer where cus_id = %s;"
    logger.debug(cursor.mogrify(query, (cus_id,)))
    cursor.execute(query, (cus_id, ))
    result = cursor.fetchone()
    logger.debug(result)
    if not result:
        raise CustomerNotFound
    # We don't need to check manually due to the primary key constraints.
    # Now insert data
    try:
        query = """
            insert into account (acc_id, acc_balance, acc_type, acc_open_date)
            values (%s, 0, %s, now());
        """
        logger.debug(cursor.mogrify(query))
        cursor.execute(query, (acc_id, acc_type.value,))
        insert_account(cursor, acc_type, acc_id, sto_interest_rate, sto_currency_type)
    except pymysql.err.IntegrityError:
        ...
    insert_have_account(cursor, acc_type, cus_id, bra_name, acc_id)
    return acc_id


def get_account_info(cursor: Cursor, acc_type=None, acc_id: str = None, cus_id: str = None, bra_name: str = None):
    if not acc_type and not acc_id:
        raise ImplicitAccType
    # if given `acc_id` and not given `acc_type`, then use it to decide the `acc_type`
    if not acc_type and acc_id:
        try:
            acc_type = get_acc_type(cursor, acc_id)
        except AttributeError:
            return []
    print(acc_type)
    if acc_type == AccountType.STORE:
        query = """
            select hsa.cus_id as cus_id, acc.acc_id as acc_id, acc_balance, acc_type,
                sa.sto_interest_rate as sto_interest_rate, sa.sto_currency_type as sto_currency_type,
                hsa.bra_name as bra_name, hsa.sto_last_visit_date as sto_last_visit_date, acc_open_date
                from account as acc, store_account as sa, have_store_account as hsa
            where acc.acc_id = sa.acc_id and acc.acc_id = hsa.acc_id
        """
    elif acc_type == AccountType.CHECK:
        query = """
            select hca.cus_id as cus_id, acc.acc_id as acc_id, acc_balance, acc_type,
                ca.che_overdraft as che_overdraft,
                hca.bra_name as bra_name, hca.che_last_visit_date as che_last_visit_date, acc_open_date
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
    logger.info(query)
    result = cursor.fetchall()
    logger.info(result)
    return result


def update_last_visit_time(cursor: Cursor, acc_id: str, cus_id: int, date=None):
    if date:
        raise Unimplemented
    acc_type = get_acc_type(cursor, acc_id)
    if acc_type == AccountType.STORE:
        query = """update have_store_account set sto_last_visit_date = now()
                where cus_id = %(cus_id)s and acc_id = %(acc_id)s"""
        cursor.execute(query, {'cus_id': cus_id, 'acc_id': acc_id})
    elif acc_type == AccountType.CHECK:
        query = """update have_check_account set che_last_visit_date = now()
                where cus_id = %(cus_id)s and acc_id = %(acc_id)s"""
        cursor.execute(query, {'cus_id': cus_id, 'acc_id': acc_id})


def update_account(cursor: Cursor, acc_id: str, **kwargs):
    acc_type = get_acc_type(cursor, acc_id)
    acc_keys = ['acc_balance']
    acc_kwargs = {k: v for (k, v) in kwargs.items() if k in acc_keys}
    for k, v in acc_kwargs.items():
        cursor.execute(f"update account set {k} = %s where acc_id = %s;", (v, acc_id))
    if acc_type == AccountType.STORE:
        sto_keys = ['sto_interest_rate', 'sto_currency_type']
        sto_kwargs = {k: v for (k, v) in kwargs.items() if k in sto_keys}
        logger.info(f'update {sto_kwargs.keys()} for {acc_id}')
        for k, v in sto_kwargs.items():
            cursor.execute(f"update store_account set {k} = %s where acc_id = %s;", (v, acc_id))
    elif acc_type == AccountType.CHECK:
        che_keys = ['che_overdraft']
        che_kwargs = {k: v for (k, v) in kwargs.items() if k in che_keys}
        logger.info(f'update {che_kwargs.keys()} for {acc_id}')
        for k, v in che_kwargs.items():
            cursor.execute(f"update check_account set {k} = %s where acc_id = %s;", (v, acc_id))
    else:
        raise UnknownAccountType


def get_balance(cursor: Cursor, acc_id: str):
    cursor.execute('select acc_balance from account where acc_id = %s', (acc_id, ))
    return cursor.fetchone().get('acc_balance')


def get_overdraft(cursor: Cursor, acc_id: str):
    cursor.execute('select che_overdraft from check_account where acc_id = %s', (acc_id, ))
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


def remove_have_account(cursor: Cursor, acc_id: str, cus_id: str, bra_name: str, **kwargs):
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
    logger.info(f'left relation: {acc_info}')
    if len(acc_info) == 0:
        remove_account(cursor, acc_id, cascade=True)



