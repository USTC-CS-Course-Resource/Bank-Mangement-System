import pymysql
from pymysql.connections import Connection
from pymysql.cursors import Cursor
from bankdb.err import *
from bankdb.checker import is_valid_arg
from utils.logger import Logger
from typing import List
import pandas as pd
from enum import Enum


logger = Logger.get_logger()


class LoanState(Enum):
    DONE = 0
    PAYING = 1


def insert_loan(cursor: Cursor, bra_name: str, loa_amount: float) -> int:
    cursor.execute("insert into loan (bra_name, loa_amount) values (%s, %s)", (bra_name, loa_amount))
    cursor.execute("select last_insert_id() as id;")
    loa_id = cursor.fetchone().get('id')
    return loa_id


def insert_pay_loan(cursor: Cursor, loa_id: int, loa_pay_amount: float) -> int:
    if get_loan_state(cursor, loa_id) == LoanState.DONE:
        raise LoanAlreadyDone
    cursor.execute("insert into pay_loan (loa_id, loa_pay_amount, loa_pay_date) values (%s, %s, now())",
                   (loa_id, loa_pay_amount))
    cursor.execute("select last_insert_id() as id;")
    loa_pay_id = cursor.fetchone().get('id')
    return loa_pay_id


def insert_loan_with_relations(cursor: Cursor, cus_ids: List[str], bra_name: str, loa_amount: float) -> int:
    loa_id = insert_loan(cursor, bra_name, loa_amount)
    for cus_id in cus_ids:
        cursor.execute("insert into loan_relation (cus_id, loa_id) values(%s, %s)", (cus_id, loa_id))
    return loa_id


def get_pay_load_records(cursor: Cursor, loa_id: int) -> pd.DataFrame:
    cursor.execute("select loa_pay_id, loa_id, loa_pay_amount, loa_pay_date from pay_loan where loa_id = %s", (loa_id,))
    pay_loan_records = cursor.fetchall()
    pay_loan_records = pd.DataFrame(pay_loan_records,
                                    columns=('loa_pay_id', 'loa_id', 'loa_pay_amount', 'loa_pay_date'))
    return pay_loan_records


def get_loa_amount(cursor: Cursor, loa_id: int) -> float:
    cursor.execute("select loa_amount from loan where loa_id = %s", (loa_id,))
    return cursor.fetchone().get('loa_amount')


def get_loan_state(cursor: Cursor, loa_id: int):
    pay_loan_records = get_pay_load_records(cursor, loa_id)
    loa_amount = get_loa_amount(cursor, loa_id)
    if pay_loan_records.get('loa_pay_amount').sum() == loa_amount:
        return LoanState.DONE
    else:
        return LoanState.PAYING


def remove_loan_with_relations(cursor: Cursor, loa_id: int):
    if get_loan_state(cursor, loa_id) == LoanState.PAYING:
        raise LoanBeingPayed
    cursor.execute('delete from loan_relation where loa_id = %s', (loa_id,))
    cursor.execute('delete from pay_loan where loa_id = %s', (loa_id,))
    cursor.execute('delete from loan where loa_id = %s', (loa_id,))