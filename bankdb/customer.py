from pymysql.cursors import Cursor
from utils.err import *
from bankdb.checker import is_valid_arg
from utils.logger import Logger

logger = Logger.get_logger('bankdb')


def insert_customer_with_contacts(
        cursor: Cursor,
        cus_id: str = None, cus_name: str = None, cus_phone: str = None, cus_address: str = None,
        con_name: str = None, con_phone: str = None, con_email: str = None, con_relation: str = None):
    kwargs = {
        'cus_id': cus_id, 'cus_name': cus_name, 'cus_phone': cus_phone, 'cus_address': cus_address,
        'con_name': con_name, 'con_phone': con_phone, 'con_email': con_email, 'con_relation': con_relation
    }
    for k, v in kwargs.items():
        if not is_valid_arg(k):
            raise ArgFormatException
    # insert customer
    query = """
        insert into customer (cus_id, cus_name, cus_phone, cus_address)
        values (%(cus_id)s, %(cus_name)s, %(cus_phone)s, %(cus_address)s);
    """
    logger.info(cursor.mogrify(query, kwargs))
    cursor.execute(query, kwargs)
    # insert corresponding contacts
    query = """
        insert into contacts (cus_id, con_name, con_phone, con_email, con_relation)
        values (%(cus_id)s, %(con_name)s, %(con_phone)s, %(con_email)s, %(con_relation)s);
    """
    logger.info(cursor.mogrify(query, kwargs))
    cursor.execute(query, kwargs)


def remove_customer_with_contacts(cursor: Cursor, cus_id: str):
    # check if still has store account
    query = """
        select count(*) as count from have_store_account
            where have_store_account.cus_id = cus_id;
    """
    cursor.execute(query)
    count = cursor.fetchone().get('count')
    if count > 0:
        raise StillHasAccount
    # check if still has check account
    query = """
        select count(*) as count from have_check_account
            where have_check_account.cus_id = cus_id;
    """
    cursor.execute(query)
    count = cursor.fetchone().get('count')
    if count > 0:
        raise StillHasAccount
    # check if still has loan
    query = """
        select count(*) as count from loan_relation
            where loan_relation.cus_id = cus_id;
    """
    cursor.execute(query)
    count = cursor.fetchone().get('count')
    if count > 0:
        raise StillHasLoan
    # if everything is ok, remove the customer and contacts
    query = "delete from contacts where contacts.cus_id = %(cus_id)s;"
    cursor.execute(query, {'cus_id': cus_id})
    query = "delete from customer where customer.cus_id = %(cus_id)s;"
    cursor.execute(query, {'cus_id': cus_id})


def get_customer_with_contacts(cursor: Cursor, cus_id: str = None):
    if cus_id:
        query = """
            select cus.cus_id as cus_id, cus_name, cus_phone, cus_address, 
            con_name, con_phone, con_email, con_relation
            from customer as cus, contacts as con
            where con.cus_id = cus.cus_id and cus.cus_id = %s;
        """
        cursor.execute(query, cus_id)
    else:
        query = """
            select cus.cus_id as cus_id, cus_name, cus_phone, cus_address, 
            con_name, con_phone, con_email, con_relation
            from customer as cus, contacts as con
            where cus.cus_id = con.cus_id;
        """
        cursor.execute(query)
    result = cursor.fetchall()
    if cus_id:
        assert len(result) <= 1
    return result


def update_customer_with_contacts(cursor: Cursor, cus_id: str, **kwargs):
    cus_keys = ['cus_name', 'cus_phone', 'cus_address']
    con_keys = ['con_name', 'con_phone', 'con_email', 'con_relation']
    cus_kwargs = {k: v for k, v in kwargs.items() if k in cus_keys}
    con_kwargs = {k: v for k, v in kwargs.items() if k in con_keys}
    dropped_keys = [k for k in kwargs if k not in cus_keys and k not in con_keys]
    if dropped_keys:
        logger.warn(f'drop keys: {dropped_keys}')
    # update customer or contacts
    # It is safe to write k into the query sql because it is constrained by `*_key`
    for k, v in cus_kwargs.items():
        if not is_valid_arg(k):
            raise ArgFormatException
        query = f"update customer set {k} = %s where cus_id = %s;"
        logger.debug(cursor.mogrify(query, (v, cus_id)))
        cursor.execute(query, (v, cus_id))
    for k, v in con_kwargs.items():
        if not is_valid_arg(k):
            raise ArgFormatException
        query = f"update contacts set {k} = %s where cus_id = %s;"
        logger.debug(cursor.mogrify(query, (v, cus_id)))
        cursor.execute(query, (v, cus_id))
