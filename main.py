import pymysql
import argparse
from pymysql.connections import Connection
from bankdb import customer


def parse_args():
    parser = argparse.ArgumentParser(description="Bank Database System")
    # parser.add_argument("--dataset", nargs="?", default="mutag", help="Choose a dataset:[mutag, reddit, vg]")
    # parser.add_argument('--topk', type=float, default=0.1, help='top k ratio')
    # parser.add_argument('-s', '--sas', default=False, help='sample action space', action="store_true")
    # parser.add_argument('-t', "--test", nargs="+", default=['bankdb'], help="module to test: [bankdb]")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    connection = Connection(host='localhost',
                            user='root',
                            password='',
                            database='bank',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
    # customer.remove_customer_with_contacts(connection, '350500200001011111')
    # customer.get_customer_with_contacts(connection, '350500200001011111')
    # customer.insert_customer_with_contacts(connection,
    #                                        '350500200001011111',
    #                                        '小憨憨',
    #                                        '123456',
    #                                        '憨憨家',
    #                                        '小恐龙',
    #                                        '181111',
    #                                        '666@hanhan.com',
    #                                        '情侣')
    # customer.get_customer_with_contacts(connection, '350500200001011111')
