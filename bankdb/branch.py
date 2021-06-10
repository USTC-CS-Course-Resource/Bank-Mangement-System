from pymysql.connections import Connection
from pymysql.cursors import Cursor
from utils.logger import Logger

logger = Logger.get_logger('bankdb')


def insert_branch(cursor: Cursor, bra_name: str, bra_city: str):
    query = """
        insert into branch (bra_name, bra_city)
        values (%(bra_name)s, %(bra_city)s);
    """
    cursor.execute(query, {'bra_name': bra_name, 'bra_city': bra_city})

