import pymysql
import os.path as osp
from pymysql.connections import Connection
from bankdb.err import *
from bankdb import logger


def insert_customer_with_contacts(
        conn: Connection,
        cus_id: str = None, cus_name: str = None, cus_phone: str = None, cus_address: str = None,
        con_name: str = None, con_phone: str = None, con_email: str = None, con_relation: str = None):
    with conn.cursor() as cursor:
        kwargs = {
            'cus_id': cus_id, 'cus_name': cus_name, 'cus_phone': cus_phone, 'cus_address': cus_address,
            'con_name': con_name, 'con_phone': con_phone, 'con_email': con_email, 'con_relation': con_relation
        }
        # insert customer
        query = """
            insert into customer (id, name, phone, address)
            values (%(cus_id)s, %(cus_name)s, %(cus_phone)s, %(cus_address)s);
        """
        cursor.execute(query, kwargs)
        # insert corresponding contacts
        query = """
            insert into contacts (cus_id, name, phone, email, relation)
            values (%(cus_id)s, %(con_name)s, %(con_phone)s, %(con_email)s, %(con_relation)s);
        """
        cursor.execute(query, kwargs)
        conn.commit()


def remove_customer_with_contacts(conn: Connection, cus_id: str):
    with conn.cursor() as cursor:
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
        try:
            query = "delete from contacts where contacts.cus_id = %(cus_id)s;"
            cursor.execute(query, {'cus_id': cus_id})
            query = "delete from customer where customer.id = %(cus_id)s;"
            cursor.execute(query, {'cus_id': cus_id})
        except pymysql.err.MySQLError as e:
            conn.rollback()
        else:
            conn.commit()


def get_customer_with_contacts(conn: Connection, cus_id: str = None):
    with conn.cursor() as cursor:
        if cus_id:
            query = "select * from customer, contacts where customer.id = contacts.cus_id and customer.id = %s;"
            cursor.execute(query, cus_id)
        else:
            query = "select * from customer, contacts where customer.id = contacts.cus_id;"
            cursor.execute(query)
        result = cursor.fetchall()
        logger.info(result)
    return result


def update_customer_with_contacts(
        conn: Connection, cus_id: str, **kwargs):
    cus_keys = ['cus_name', 'cus_phone', 'cus_address']
    con_keys = ['con_name', 'con_phone', 'con_email', 'con_relation']
    cus_kwargs = {k[4:]: v for k, v in kwargs.items() if k in cus_keys}
    con_kwargs = {k[4:]: v for k, v in kwargs.items() if k in con_keys}
    dropped_keys = [k for k in kwargs if k not in cus_keys and k not in con_keys]
    if dropped_keys:
        logger.warn(f'drop keys: {dropped_keys}')
    with conn.cursor() as cursor:
        # update customer or contacts
        # It is safe to write k into the query sql because it is constrained by `*_key`
        for k, v in cus_kwargs.items():
            query = f"""
                update customer set {k} = %s
                where id = %s;
            """
            logger.debug(cursor.mogrify(query, (v, cus_id)))
            cursor.execute(query, (v, cus_id))
        for k, v in con_kwargs.items():
            query = f"""
                update contacts set {k} = %s
                where cus_id = %s;
            """
            logger.debug(cursor.mogrify(query, (v, cus_id)))
            cursor.execute(query, (v, cus_id))
        conn.commit()
