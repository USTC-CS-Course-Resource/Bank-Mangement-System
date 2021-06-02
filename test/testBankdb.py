import unittest
import pymysql
from pymysql.connections import Connection
from bankdb import customer, account, branch
from utils.logger import *
from utils.logger import Logger
import bankdb
import datetime

unittest.TestLoader.sortTestMethodsUsing = None
logger = Logger.get_logger()


class TestBankdb(unittest.TestCase):
    conn = Connection(host='localhost',
                      user='root',
                      password='',
                      database='bank',
                      charset='utf8mb4',
                      cursorclass=pymysql.cursors.DictCursor)
    customer_with_contacts_data = [
        {'cus_id': '350500200001011111', 'cus_name': '小憨憨', 'cus_phone': '123456',
         'cus_address': '憨憨家', 'con_name': '小恐龙', 'con_phone': '181111',
         'con_email': '666@hanhan.com', 'con_relation': '情侣'}
    ]

    def test_remove_insert_update_customer(self):
        data = self.customer_with_contacts_data[0]
        # clear
        bankdb._clear_table(self.conn,
                            ['have_store_account', 'store_account', 'account', 'branch', 'contacts', 'customer'])
        # insert
        customer.insert_customer_with_contacts(self.conn, **data)
        result = customer.get_customer_with_contacts(self.conn, '350500200001011111')
        self.assertEqual(result, [data])
        # update
        customer.update_customer_with_contacts(self.conn, cus_id='350500200001011111', cus_name='大憨憨', con_name='大恐龙')
        result = customer.get_customer_with_contacts(self.conn, '350500200001011111')
        data['cus_name'] = '大憨憨'
        data['con_name'] = '大恐龙'
        self.assertEqual(result, [data])
        # remove
        customer.remove_customer_with_contacts(self.conn, '350500200001011111')
        result = customer.get_customer_with_contacts(self.conn, '350500200001011111')
        self.assertEqual(result, ())

    def test_open_account(self):
        # 0.0. clear
        bankdb._clear_table(self.conn,
                            ['have_store_account', 'store_account', 'account', 'branch', 'contacts', 'customer'])
        # 0.1. insert branch and customer
        branch.insert_branch(self.conn, bra_name='憨憨银行合肥分行', bra_city='合肥')
        customer.insert_customer_with_contacts(self.conn, **self.customer_with_contacts_data[0])
        # 1. test open account
        acc_id = account.open_account(conn=self.conn, acc_type=account.AccountType.STORE, cus_id='350500200001011111',
                                      bra_name='憨憨银行合肥分行', sto_interest_rate=0.02, sto_currency_type='CNY')
        result = account.get_account_info(self.conn, acc_id)
        result.pop('sto_last_visit_date')
        self.assertEqual(result,
                         {'cus_id': '350500200001011111', 'acc_id': acc_id, 'acc_balance': 0.0, 'acc_type': 0,
                          'sto_interest_rate': 0.02, 'sto_currency_type': 'CNY', 'bra_name': '憨憨银行合肥分行',
                          'acc_open_date': datetime.date(2021, 6, 2)})
        # 2. test remove account
        account.remove_account(conn=self.conn, acc_id=acc_id)
        result = customer.get_customer_with_contacts(self.conn, '350500200001011111')
        self.assertEqual(result, self.customer_with_contacts_data)
        # 0.2. clear
        bankdb._clear_table(self.conn,
                            ['have_store_account', 'store_account', 'account', 'branch', 'contacts', 'customer'])


if __name__ == '__main__':
    # logging.disable(logging.CRITICAL)
    unittest.main()
    # logging.disable(logging.NOTSET)
