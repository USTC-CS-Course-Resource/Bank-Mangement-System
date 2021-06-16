from pymysql.cursors import Cursor
from utils.err import *
from utils import sql_datetime_format
from utils.logger import Logger
from typing import List, Union
import pandas as pd
from enum import Enum
from datetime import datetime

logger = Logger.get_logger('bankdb')


class LoanState(Enum):
    DONE = 0
    PAYING = 1


def insert_loan(cursor: Cursor, bra_name: str, loa_amount: float) -> int:
    cursor.execute("insert into loan (bra_name, loa_amount) values (%s, %s)", (bra_name, loa_amount))
    cursor.execute("select last_insert_id() as id;")
    loa_id = cursor.fetchone().get('id')
    return loa_id


def insert_pay_loan(cursor: Cursor, loa_id: int, loa_pay_amount: float, date: datetime) -> int:
    if get_loan_state(cursor, loa_id) == LoanState.DONE:
        raise LoanAlreadyDone
    loa_pay_amount_sum = get_loa_pay_amount_sum(cursor, loa_id)
    if loa_pay_amount_sum + loa_pay_amount > get_loa_amount(cursor, loa_id):
        raise PayTooMuch
    cursor.execute("insert into pay_loan (loa_id, loa_pay_amount, loa_pay_date) values (%s, %s, %s)",
                   (loa_id, loa_pay_amount, date))
    cursor.execute("select last_insert_id() as id;")
    loa_pay_id = cursor.fetchone().get('id')
    return loa_pay_id


def insert_loan_with_relations(cursor: Cursor, cus_ids: Union[str, List[str]], bra_name: str, loa_amount: float,
                               date: Union[datetime, str] = None) -> int:
    if type(date) is datetime:
        date = date.strftime(sql_datetime_format)
    loa_id = insert_loan(cursor, bra_name, loa_amount)
    if type(cus_ids) == str:
        cus_ids = [cus_ids]
    for cus_id in cus_ids:
        cursor.execute("insert into loan_relation (cus_id, loa_id) values(%s, %s)", (cus_id, loa_id))
        update_loan_log(cursor, bra_name, loa_id, cus_id, loa_amount, date)
    return loa_id


def search_loan(cursor: Cursor, loa_id: int = None, bra_name: str = None, cus_id: str = None, **kwargs):
    if loa_id:
        return get_loa_info(cursor, loa_id)
    if not bra_name and not cus_id:
        cursor.execute("select * from loan;")
        return cursor.fetchall()
    query = "select * from loan where "
    tmp = []
    if bra_name:
        tmp.append(cursor.mogrify("bra_name = %s", bra_name))
    if cus_id:
        tmp.append(cursor.mogrify("loa_id in (select loa_id from loan_relation where cus_id = %s)", cus_id))
    query += ' and '.join(tmp) + ';'
    logger.info(query)
    cursor.execute(query)
    return cursor.fetchall()


def get_loa_info(cursor: Cursor, loa_id: int):
    cursor.execute("select * from loan where loa_id = %s;", (loa_id,))
    return cursor.fetchall()


def get_pay_loa_records(cursor: Cursor, loa_id: int) -> pd.DataFrame:
    cursor.execute("select loa_pay_id, loa_id, loa_pay_amount, loa_pay_date from pay_loan where loa_id = %s", (loa_id,))
    pay_loan_records = cursor.fetchall()
    return pay_loan_records


def get_loa_amount(cursor: Cursor, loa_id: int) -> float:
    cursor.execute("select loa_amount from loan where loa_id = %s", (loa_id,))
    return cursor.fetchone().get('loa_amount')


def get_loa_pay_amount_sum(cursor: Cursor, loa_id: int):
    query = """
        select sum(loa_pay_amount) as loa_pay_amount_sum 
        from loan, pay_loan where loan.loa_id = pay_loan.loa_id and loan.loa_id = %s group by (loan.loa_id);
    """
    cursor.execute(query, (loa_id,))
    loa_pay_amount_sum = cursor.fetchone()
    if loa_pay_amount_sum:
        loa_pay_amount_sum = loa_pay_amount_sum.get('loa_pay_amount_sum')
    else:
        loa_pay_amount_sum = 0
    return loa_pay_amount_sum


def get_loan_state(cursor: Cursor, loa_id: int):
    loa_amount = get_loa_amount(cursor, loa_id)
    loa_pay_amount_sum = get_loa_pay_amount_sum(cursor, loa_id)
    if loa_pay_amount_sum >= loa_amount:
        return LoanState.DONE
    else:
        return LoanState.PAYING


def get_customer_info(cursor: Cursor, loa_id: int):
    cursor.execute("select cus_id from loan_relation where loa_id = %s", (loa_id,))
    return cursor.fetchall()


def remove_loan_with_relations(cursor: Cursor, loa_id: int):
    if get_loan_state(cursor, loa_id) == LoanState.PAYING:
        raise LoanBeingPayed
    cursor.execute('delete from loan_relation where loa_id = %s', (loa_id,))
    cursor.execute('delete from pay_loan where loa_id = %s', (loa_id,))
    cursor.execute('delete from loan where loa_id = %s', (loa_id,))


def update_loan_log(cursor: Cursor, bra_name: str, loa_id: int, cus_id: str, loa_amount: float,
                    log_date: Union[datetime, str] = None):
    if type(log_date) is datetime:
        log_date = log_date.strftime(sql_datetime_format)
    query = """
        insert into 
        loan_log (bra_name, loa_id, cus_id, loa_amount, log_date)
        values   (%s, %s, %s, %s, %s);
    """
    cursor.execute(query, (bra_name, loa_id, cus_id, loa_amount, log_date))
    logger.info(f'inserted loan log: {(bra_name, loa_id, cus_id, loa_amount, log_date)}')


def get_loan_summary(cursor: Cursor):
    query = """
        select bra_name, sum(loa_amount) as loa_amount, max(log_date) as date from
           (
              select bra_name, loa_id, max(loa_amount) as loa_amount, max(log_date) as log_date from loan_log
              group by bra_name, loa_id
           ) _loan_log
        group by bra_name, year(log_date), month(log_date);
    """
    cursor.execute(query)
    loan_summary = cursor.fetchall()
    loan_summary = pd.DataFrame(loan_summary, columns=['bra_name', 'date', 'loa_amount'])
    loan_summary['date'] = loan_summary['date'].map(lambda date: str(date)[:-3])
    query = """
        select bra_name, max(log_date) as date, count(distinct cus_id) as cus_count from loan_log
        group by bra_name, year(log_date), month(log_date);
    """
    cursor.execute(query)
    cus_count_summary = cursor.fetchall()
    cus_count_summary = pd.DataFrame(cus_count_summary, columns=['bra_name', 'date', 'cus_count'])
    cus_count_summary['date'] = cus_count_summary['date'].map(lambda date: str(date)[:-3])
    summary = loan_summary.merge(cus_count_summary, on=['bra_name', 'date'])
    logger.info(f'loan summary:\n{summary}')
    return summary.to_dict('records')
