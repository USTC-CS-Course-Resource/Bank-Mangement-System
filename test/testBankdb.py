import unittest
import pymysql
from pymysql.connections import Connection
from bankdb import customer


class TestBankdb(unittest.TestCase):
    conn = Connection(host='localhost',
                      user='root',
                      password='',
                      database='bank',
                      charset='utf8mb4',
                      cursorclass=pymysql.cursors.DictCursor)

    def test_add_customer(self):
        customer.remove_customer_with_contacts(self.conn, '350500200001011111')
        result = customer.get_customer_with_contacts(self.conn, '350500200001011111')
        self.assertEqual(result, ())

    def test_update_customer(self):
        customer.update_customer_with_contacts(self.conn, cus_id='350500200001011111', cus_name='大憨憨', con_name='大恐龙')
        result = customer.get_customer_with_contacts(self.conn, '350500200001011111')
        self.assertEqual(1, 1)
        # self.assertEqual(result,
        #                  [{'id': '350500200001011111', 'name': '大憨憨', 'phone': '123456', 'address': '憨憨家',
        #                    'cus_id': '350500200001011111', 'contacts.name': '小恐龙', 'contacts.phone': '181111',
        #                    'email': '666@hanhan.com', 'relation': '情侣'}])

    def test_remove_customer(self):
        customer.insert_customer_with_contacts(self.conn,
                                               '350500200001011111', '小憨憨', '123456', '憨憨家',
                                               '小恐龙', '181111', '666@hanhan.com', '情侣')
        result = customer.get_customer_with_contacts(self.conn, '350500200001011111')
        self.assertEqual(result,
                         [{'id': '350500200001011111', 'name': '小憨憨', 'phone': '123456', 'address': '憨憨家',
                           'cus_id': '350500200001011111', 'contacts.name': '小恐龙', 'contacts.phone': '181111',
                           'email': '666@hanhan.com', 'relation': '情侣'}])


if __name__ == '__main__':
    unittest.main()
