from bankdb.err import *
import pymysql
from pymysql.connections import Connection
from pymysql.cursors import Cursor
from enum import Enum
from utils.logger import Logger

logger = Logger.get_logger()


class AccountType(Enum):
    STORE = 0
    CHECK = 1


def get_acc_type(cursor: Cursor, acc_id: int):
    cursor.execute("select acc_type from account where acc_id = %s", (acc_id,))
    return AccountType(cursor.fetchone().get('acc_type'))


def open_account(cursor: Cursor,
                 acc_type: AccountType,
                 cus_id: str, bra_name: str, sto_interest_rate: float, sto_currency_type: str = 'CNY'):
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
    query = """
        insert into account (acc_balance, acc_type, acc_open_date)
        values (0, %s, now());
    """
    logger.debug(cursor.mogrify(query))
    cursor.execute(query, (acc_type.value,))
    cursor.execute("select last_insert_id() as id;")
    acc_id = cursor.fetchone().get('id')
    if acc_type == AccountType.STORE:
        query = """
            insert into store_account(acc_id, sto_interest_rate, sto_currency_type)
            values (%s, %s, %s);
        """
        logger.debug(cursor.mogrify(query, (acc_id, sto_interest_rate, sto_currency_type)))
        cursor.execute(query, (acc_id, sto_interest_rate, sto_currency_type))
        query = """
            insert into have_store_account(cus_id, bra_name, acc_id, sto_last_visit_date)
            values (%(cus_id)s, %(bra_name)s, %(acc_id)s, now());
        """
        logger.debug(query, {'cus_id': cus_id, 'bra_name': bra_name, 'acc_id': acc_id})
        cursor.execute(query, {'cus_id': cus_id, 'bra_name': bra_name, 'acc_id': acc_id})
    return acc_id


def get_account_info(cursor: Cursor, acc_id: int):
    acc_type = get_acc_type(cursor, acc_id)
    if acc_type == AccountType.STORE:
        query = """
            select hsa.cus_id as cus_id, acc.acc_id as acc_id, acc_balance, acc_type,
                sa.sto_interest_rate as sto_interest_rate, sa.sto_currency_type as sto_currency_type,
                hsa.bra_name as bra_name, hsa.sto_last_visit_date as sto_last_visit_date, acc_open_date
                from account as acc, store_account as sa, have_store_account as hsa
            where acc.acc_id = %s and acc.acc_id = sa.acc_id and acc.acc_id = hsa.acc_id;
        """
    elif acc_type == AccountType.CHECK:
        query = """
            select hsa.cus_id as cus_id, acc.acc_id as acc_id, acc_balance, acc_type,
                sa.che_interest_rate as che_interest_rate, sa.che_currency_type as che_currency_type,
                hsa.bra_name as bra_name, hsa.che_last_visit_date as che_last_visit_date, acc_open_date
                from account as acc, check_account as ca, have_check_account as hca
            where acc.acc_id = %s and acc.acc_id = ca.acc_id and acc.acc_id = hca.acc_id;
        """
    else:
        raise UnknownAccountType
    cursor.execute(query, (acc_id,))
    result = cursor.fetchall()
    assert len(result) == 1
    result = result[0]
    logger.info(result)
    return result


def update_last_visit_time(cursor: Cursor, acc_id: int, cus_id: int, date=None):
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


def get_balance(cursor: Cursor, acc_id: int):
    cursor.execute('select acc_balance from account where acc_id = %s', (acc_id, ))
    return cursor.fetchone().get('acc_balance')


def get_overdraft(cursor: Cursor, acc_id: int):
    cursor.execute('select che_overdraft from check_account where acc_id = %s', (acc_id, ))
    return cursor.fetchone().get('che_overdraft')


def remove_account(cursor: Cursor, acc_id: int):
    acc_type = get_acc_type(cursor, acc_id)
    acc_balance = get_balance(cursor, acc_id)
    if acc_balance != 0:
        raise StillHasBalance
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


def remove_have_account(cursor: Cursor, acc_id: int, cus_id: str):
    acc_type = get_acc_type(cursor, acc_id)
    if acc_type == AccountType.STORE:
        cursor.execute("delete from have_store_account where acc_id = %s and cus_id = %s;", (acc_id, cus_id))
    elif acc_type == AccountType.CHECK:
        cursor.execute("delete from have_check_account where acc_id = %s and cus_id = %s;", (acc_id, cus_id))
    else:
        raise UnknownAccountType



