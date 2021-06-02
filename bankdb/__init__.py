import pymysql
from pymysql.connections import Connection
from bankdb.err import *
from checker import is_valid_arg
from typing import Union, List
from utils.logger import Logger

logger = Logger.get_logger()


def _clear_table(conn: Connection, names: Union[str, List[str]]):
    # TODO assert for table names
    with conn.cursor() as cursor:
        if type(names) == str:
            names = [names]

        for name in names:
            # logger.debug(cursor.mogrify(f'delete from {name};'))
            cursor.execute(f'delete from {name};')
            conn.commit()

