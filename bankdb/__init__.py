import pymysql
from pymysql.connections import Connection
from pymysql.cursors import Cursor
from bankdb.err import *
from bankdb.checker import is_valid_arg
from typing import Union, List
from utils.logger import Logger

logger = Logger.get_logger()


def _clear_table(cursor: Cursor, names: Union[str, List[str]]):
    # TODO assert for table names
    if type(names) == str:
        names = [names]

    for name in names:
        cursor.execute(f'delete from {name};')

