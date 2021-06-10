from pymysql.cursors import Cursor
from bankdb.checker import is_valid_arg
from typing import Union, List
from utils.logger import Logger
from . import account
from . import branch
from . import checker
from . import customer
from utils import err
from . import loan

logger = Logger.get_logger('bankdb')


def clear_table(cursor: Cursor, names: Union[str, List[str]]):
    # TODO assert for table names
    if type(names) == str:
        names = [names]

    for name in names:
        cursor.execute(f'delete from {name};')


__name__ = [account,
            branch,
            checker,
            customer,
            err,
            loan,
            clear_table]
