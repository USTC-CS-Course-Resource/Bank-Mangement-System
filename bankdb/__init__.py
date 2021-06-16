from pymysql.cursors import Cursor
from bankdb.checker import is_valid_arg
from typing import Union, List
import os.path as osp
from utils.logger import Logger
from . import account
from . import branch
from . import checker
from . import customer
from . import loan
from utils import err, execute_sql, sql_datetime_format, sql_str2datetime
from datetime import datetime

logger = Logger.get_logger('bankdb')

all_tables = ['have_check_account',
              'have_store_account',
              'check_account',
              'store_account',
              'account',
              'pay_loan',
              'loan_relation',
              'loan',
              'responsibility',
              'department_manager',
              'staff',
              'department',
              'contacts',
              'customer',
              'branch',
              'account_log',
              'account_update_log',
              'loan_log']


def clear_table(cursor: Cursor, tables: Union[str, List[str]]):
    if type(tables) == str:
        tables = [tables]

    for table in tables:
        cursor.execute(f'delete from {table};')


def drop_tables(cursor: Cursor, tables: Union[str, List[str]]):
    if type(tables) == str:
        tables = [tables]

    for table in tables:
        cursor.execute(f'drop table if exists {table};')
        logger.info(f'dropped table {table} (if exists)')


def initialize(cursor: Cursor):
    drop_tables(cursor, all_tables)
    execute_sql(cursor, osp.join(osp.dirname(__file__), '..', 'design', 'log.sql'))
    logger.info(f'initialized account log tables')
    execute_sql(cursor, osp.join(osp.dirname(__file__), '..', 'design', 'powerdesigner-models', 'crebas.sql'))
    logger.info(f'initialized bankdb tables')
    # clear_table(cursor, all_tables)
    branch.insert_branch(cursor, bra_name='憨憨银行合肥分行', bra_city='合肥')
    branch.insert_branch(cursor, bra_name='憨憨银行泉州分行', bra_city='泉州')
    customer.insert_customer_with_contacts(cursor, cus_id='350500200001011111', cus_name='小憨憨', cus_phone='123456',
                                           cus_address='小憨憨家', con_name='小珑珑', con_phone='181111',
                                           con_email='6661@hanhan.com', con_relation='情侣')
    customer.insert_customer_with_contacts(cursor, cus_id='350500200001011112', cus_name='中憨憨', cus_phone='123456',
                                           cus_address='中憨憨家', con_name='中珑珑', con_phone='181111',
                                           con_email='6662@hanhan.com', con_relation='情侣')
    customer.insert_customer_with_contacts(cursor, cus_id='350500200001011113', cus_name='大憨憨', cus_phone='123456',
                                           cus_address='大憨憨家', con_name='大珑珑', con_phone='181111',
                                           con_email='6663@hanhan.com', con_relation='情侣')
    customer.insert_customer_with_contacts(cursor, cus_id='350500200001011114', cus_name='超级憨憨', cus_phone='123456',
                                           cus_address='超级憨憨家', con_name='超级珑珑', con_phone='181111',
                                           con_email='6663@hanhan.com', con_relation='情侣')
    logger.info("It's 2020-07")
    account.open_account(cursor,
                         acc_id='0000000000000001', acc_type=account.AccountType.STORE,
                         cus_id='350500200001011111', bra_name='憨憨银行合肥分行', sto_interest_rate=0.06,
                         sto_currency_type='CNY', date=datetime.strptime("2020-07-16 09:00:00", sql_datetime_format))
    account.update_account(cursor, acc_id='0000000000000001', cus_id='350500200001011111', acc_balance=66,
                           date=sql_str2datetime("2020-07-20 09:00:00"))
    logger.info("It's 2020-08")
    loan.insert_loan_with_relations(cursor, cus_ids=['350500200001011111', '350500200001011112'],
                                    bra_name='憨憨银行合肥分行', loa_amount=666,
                                    date=sql_str2datetime("2020-08-03 09:00:00"))
    account.open_account(cursor,
                         acc_id='0000000000000002', acc_type=account.AccountType.STORE,
                         cus_id='350500200001011112', bra_name='憨憨银行合肥分行', sto_interest_rate=0.06,
                         sto_currency_type='CNY', date=sql_str2datetime("2020-08-22 09:00:00"))
    account.update_account(cursor, acc_id='0000000000000002', cus_id='350500200001011112', acc_balance=6666,
                           date=sql_str2datetime("2020-08-25 09:00:00"))
    account.update_account(cursor, acc_id='0000000000000001', cus_id='350500200001011111', acc_balance=6,
                           date=sql_str2datetime("2020-08-30 09:00:00"))
    loan.insert_loan_with_relations(cursor, cus_ids=['350500200001011111'],
                                    bra_name='憨憨银行合肥分行', loa_amount=333,
                                    date=sql_str2datetime("2020-08-30 09:00:00"))
    logger.info("It's 2020-09")
    account.update_account(cursor, acc_id='0000000000000002', cus_id='350500200001011112', acc_balance=777,
                           date=sql_str2datetime("2020-09-25 09:00:00"))
    account.update_account(cursor, acc_id='0000000000000001', cus_id='350500200001011111', acc_balance=75,
                           date=sql_str2datetime("2020-09-30 09:00:00"))
    loan.insert_loan_with_relations(cursor, cus_ids=['350500200001011112'],
                                    bra_name='憨憨银行合肥分行', loa_amount=777,
                                    date=sql_str2datetime("2020-09-30 09:00:00"))
    logger.info("It's 2020-10")
    account.open_account(cursor,
                         acc_id='0000000000000020', acc_type=account.AccountType.CHECK, cus_id='350500200001011112',
                         bra_name='憨憨银行合肥分行', date=sql_str2datetime("2020-10-02 09:00:00"))
    account.update_account(cursor, acc_id='0000000000000020', cus_id='350500200001011112',
                           acc_balance=0, che_overdraft=66,
                           date=sql_str2datetime("2020-10-15 09:00:00"))
    logger.info("It's 2020-11")
    account.update_account(cursor, acc_id='0000000000000002', cus_id='350500200001011112', acc_balance=66,
                           date=sql_str2datetime("2020-11-25 09:00:00"))
    account.update_account(cursor, acc_id='0000000000000001', cus_id='350500200001011111', acc_balance=6,
                           date=sql_str2datetime("2020-11-30 09:00:00"))
    loan.insert_loan_with_relations(cursor, cus_ids=['350500200001011113'],
                                    bra_name='憨憨银行合肥分行', loa_amount=999,
                                    date=sql_str2datetime("2020-11-30 09:00:00"))
    logger.info("It's 2020-12")
    account.update_account(cursor, acc_id='0000000000000002', cus_id='350500200001011112', acc_balance=6666,
                           date=sql_str2datetime("2020-12-25 09:00:00"))
    account.update_account(cursor, acc_id='0000000000000001', cus_id='350500200001011111', acc_balance=3333,
                           date=sql_str2datetime("2020-12-30 09:00:00"))
    logger.info("It's 2021-01")
    account.open_account(cursor,
                         acc_id='0000000000000003', acc_type=account.AccountType.STORE,
                         cus_id='350500200001011113', bra_name='憨憨银行合肥分行', sto_interest_rate=0.06,
                         sto_currency_type='CNY', date=sql_str2datetime("2021-01-21 09:00:00"))
    account.update_account(cursor, acc_id='0000000000000002', cus_id='350500200001011112', acc_balance=6666,
                           date=sql_str2datetime("2021-01-25 09:00:00"))
    account.update_account(cursor, acc_id='0000000000000001', cus_id='350500200001011111', acc_balance=6666,
                           date=sql_str2datetime("2021-01-30 09:00:00"))
    account.update_account(cursor, acc_id='0000000000000003', cus_id='350500200001011113', acc_balance=6666,
                           date=sql_str2datetime("2021-01-26 09:00:00"))
    logger.info("It's 2021-02")
    account.update_account(cursor, acc_id='0000000000000002', cus_id='350500200001011112', acc_balance=0,
                           date=sql_str2datetime("2021-02-25 09:00:00"))
    account.remove_have_account(cursor, cus_id='350500200001011112', acc_id='0000000000000002',
                                bra_name='憨憨银行合肥分行', date=sql_str2datetime("2021-02-26 09:00:00"))
    loan.insert_loan_with_relations(cursor, cus_ids=['350500200001011114', '350500200001011113'],
                                    bra_name='憨憨银行合肥分行', loa_amount=555,
                                    date=sql_str2datetime("2021-02-27 09:00:00"))
    logger.info("It's 2021-03")
    account.open_account(cursor,
                         acc_id='0000000000000040', acc_type=account.AccountType.CHECK, cus_id='350500200001011114',
                         bra_name='憨憨银行泉州分行', date=sql_str2datetime("2021-03-02 09:00:00"))
    account.open_account(cursor,
                         acc_id='0000000000000004', acc_type=account.AccountType.STORE,
                         cus_id='350500200001011114', bra_name='憨憨银行泉州分行', sto_interest_rate=0.06,
                         sto_currency_type='CNY', date=sql_str2datetime("2021-03-05 09:00:00"))
    logger.info("It's 2021-04")
    account.update_account(cursor, acc_id='0000000000000040', cus_id='350500200001011114',
                           acc_balance=77, che_overdraft=0,
                           date=sql_str2datetime("2021-04-15 09:00:00"))
    account.update_account(cursor, acc_id='0000000000000004', cus_id='350500200001011114',
                           acc_balance=666,
                           date=sql_str2datetime("2021-04-15 09:00:00"))
    loan.insert_loan_with_relations(cursor, cus_ids=['350500200001011111'],
                                    bra_name='憨憨银行合肥分行', loa_amount=666,
                                    date=sql_str2datetime("2021-04-27 09:00:00"))


__name__ = [account,
            branch,
            checker,
            customer,
            err,
            loan,
            clear_table,
            initialize]
