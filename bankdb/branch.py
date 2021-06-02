from pymysql.connections import Connection
from utils.logger import Logger

logger = Logger.get_logger()


def insert_branch(conn: Connection, bra_name: str, bra_city: str):
    with conn.cursor() as cursor:
        query = """
            insert into branch (bra_name, bra_city)
            values (%(bra_name)s, %(bra_city)s);
        """
        cursor.execute(query, {'bra_name': bra_name, 'bra_city': bra_city})
        conn.commit()

