import pymysql
import argparse
from pymysql.connections import Connection
from bankdb import customer
from test.testBankdb import TestBankdb
from utils.logger import *


def parse_args():
    parser = argparse.ArgumentParser(description="Bank Database System")
    # parser.add_argument("--dataset", nargs="?", default="mutag", help="Choose a dataset:[mutag, reddit, vg]")
    # parser.add_argument('--topk', type=float, default=0.1, help='top k ratio')
    # parser.add_argument('-s', '--sas', default=False, help='sample action space', action="store_true")
    # parser.add_argument('-t', "--test", nargs="+", default=['bankdb'], help="module to test: [bankdb]")
    args = parser.parse_args()
    return args


from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    args = parse_args()
    conn = Connection(host='localhost',
                      user='root',
                      password='',
                      database='bank',
                      charset='utf8mb4',
                      cursorclass=pymysql.cursors.DictCursor)

