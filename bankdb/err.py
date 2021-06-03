from contextlib import contextmanager
import pymysql
from pymysql.connections import Connection
from utils.logger import Logger

logger = Logger.get_logger()


@contextmanager
def cursor_with_exception_handler(conn: Connection, tx=False):
    try:
        yield conn.cursor()
    except StillHasAccount as e:
        logger.error(e)
        if tx:
            conn.rollback()
    except StillHasLoan as e:
        logger.error(e)
        if tx:
            conn.rollback()
    except ArgFormatException as e:
        logger.error(e)
        if tx:
            conn.rollback()
    except CustomerNotFound as e:
        logger.error(e)
        if tx:
            conn.rollback()
    except MultiAccount as e:
        logger.error(e)
        if tx:
            conn.rollback()
    except UnknownAccountType as e:
        logger.error(e)
        if tx:
            conn.rollback()
    except Unimplemented as e:
        logger.error(e)
        if tx:
            conn.rollback()
    except pymysql.err.MySQLError as e:
        logger.error(e)
        if tx:
            conn.rollback()
    else:
        if tx:
            conn.commit()
    finally:
        conn.cursor().close()


class StillHasAccount(Exception):
    ...


class StillHasLoan(Exception):
    ...


class ArgFormatException(Exception):
    ...


class CustomerNotFound(Exception):
    ...


class MultiAccount(Exception):
    ...


class UnknownAccountType(Exception):
    ...


class Unimplemented(Exception):
    ...

