import unittest
from pymysql.cursors import Cursor
from bankdb import customer, account, branch, loan
import bankdb
from utils.err import *

unittest.TestLoader.sortTestMethodsUsing = None
logger = Logger.get_logger('bankdb')


class TestBankdb(unittest.TestCase):
    conn = Connection(host='localhost',
                      user='root',
                      password='',
                      database='bank',
                      charset='utf8mb4',
                      cursorclass=pymysql.cursors.DictCursor)
    customer_with_contacts_data = [
        {'cus_id': '350500200001011111', 'cus_name': '小憨憨', 'cus_phone': '123456',
         'cus_address': '憨憨家', 'con_name': '小珑珑', 'con_phone': '181111',
         'con_email': '666@hanhan.com', 'con_relation': '情侣'}
    ]

    @staticmethod
    def prepare_customer(cursor: Cursor):
        # 0.0. clear
        bankdb.clear_table(cursor,
                            ['have_store_account', 'store_account', 'account', 'branch', 'contacts', 'customer'])
        # 0.1. insert branch and customer
        branch.insert_branch(cursor, bra_name='憨憨银行合肥分行', bra_city='合肥')
        customer.insert_customer_with_contacts(cursor, **TestBankdb.customer_with_contacts_data[0])

    def test_remove_insert_update_customer(self):
        with cursor_with_exception_handler(self.conn) as cursor:
            data = self.customer_with_contacts_data[0]
            # clear
            bankdb.clear_table(cursor,
                                ['have_store_account', 'store_account', 'account', 'branch', 'contacts', 'customer'])
            # insert
            customer.insert_customer_with_contacts(cursor, **data)
            result = customer.get_customer_with_contacts(cursor, '350500200001011111')
            self.assertEqual(result, [data])
            # update
            customer.update_customer_with_contacts(cursor, cus_id='350500200001011111', cus_name='大憨憨', con_name='大珑珑')
            result = customer.get_customer_with_contacts(cursor, '350500200001011111')
            data['cus_name'] = '大憨憨'
            data['con_name'] = '大珑珑'
            self.assertEqual(result, [data])
            # remove
            customer.remove_customer_with_contacts(cursor, '350500200001011111')
            result = customer.get_customer_with_contacts(cursor, '350500200001011111')
            self.assertEqual(result, ())

    def test_account(self):
        with cursor_with_exception_handler(self.conn) as cursor:
            # 0. prepare the customer
            TestBankdb.prepare_customer(cursor)
            # 1. test open account
            acc_id = account.open_account(cursor=cursor, acc_id="0000000000000000", acc_type=account.AccountType.STORE,
                                          cus_id='350500200001011111', bra_name='憨憨银行合肥分行',
                                          sto_interest_rate=0.02, sto_currency_type='CNY')
            result = account.get_account_info(cursor, acc_id)[0]
            result.pop('sto_last_visit_date')
            result.pop('acc_open_date')
            self.assertEqual(result,
                             {'cus_id': '350500200001011111', 'acc_id': acc_id, 'acc_balance': 0.0, 'acc_type': 0,
                              'sto_interest_rate': 0.02, 'sto_currency_type': 'CNY', 'bra_name': '憨憨银行合肥分行'})
            # 2. test remove account
            account.remove_account(cursor=cursor, acc_id=acc_id)
            result = customer.get_customer_with_contacts(cursor, '350500200001011111')
            self.assertEqual(result, self.customer_with_contacts_data)
            # 3. clear used tables
            bankdb.clear_table(cursor,
                                ['have_store_account', 'store_account', 'account', 'branch', 'contacts', 'customer'])

    def test_loan(self):
        with cursor_with_exception_handler(self.conn) as cursor:
            # 0. prepare the customer
            TestBankdb.prepare_customer(cursor)
            # 1. test insert loan
            loa_id = loan.insert_loan_with_relations(cursor,
                                                     cus_ids=['350500200001011111'],
                                                     bra_name='憨憨银行合肥分行',
                                                     loa_amount=66666)
            # 2. pay loan
            loan.insert_pay_loan(cursor, loa_id, 66)
            loan.insert_pay_loan(cursor, loa_id, 666)
            # 3. get pay loan information
            state = loan.get_loan_state(cursor, loa_id)
            # 4. pay until done and test
            loan.insert_pay_loan(cursor, loa_id, 65934)
            exception = None
            try:
                loan.insert_pay_loan(cursor, loa_id, 6666)
            except Exception as e:
                exception = e
            logger.info('[LoanAlreadyDone] ok')
            self.assertIsInstance(exception, LoanAlreadyDone)
            # 5. clear
            bankdb.clear_table(cursor,
                                ['pay_loan', 'loan_relation', 'loan', 'branch', 'contacts', 'customer'])


if __name__ == '__main__':
    # logging.disable(logging.CRITICAL)
    unittest.main()
    # logging.disable(logging.NOTSET)
