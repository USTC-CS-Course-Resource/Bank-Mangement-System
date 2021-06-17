from contextlib import contextmanager
import pymysql
from pymysql.connections import Connection
from utils.logger import Logger

logger = Logger.get_logger('bankdb')


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
    except StillHasBalance as e:
        logger.error(e)
        if tx:
            conn.rollback()
    except StillHasOverdraft as e:
        logger.error(e)
        if tx:
            conn.rollback()
    except LoanAlreadyDone as e:
        logger.error(e)
        if tx:
            conn.rollback()
    except LoanBeingPayed as e:
        logger.error(e)
        if tx:
            conn.rollback()
    except pymysql.err.IntegrityError as e:
        logger.error(e)
        if tx:
            conn.rollback()
        yield 'fuck'
    except Exception as e:
        logger.error(e)
        if tx:
            conn.rollback()
    else:
        if tx:
            conn.commit()
    finally:
        conn.cursor().close()


class StillHasAccount(RuntimeError):
    ...


class StillHasLoan(RuntimeError):
    ...


class ArgFormatException(RuntimeError):
    ...


class CustomerNotFound(RuntimeError):
    ...


class MultiAccount(RuntimeError):
    ...


class UnknownAccountType(RuntimeError):
    ...


class Unimplemented(RuntimeError):
    ...


class StillHasBalance(RuntimeError):
    ...


class StillHasOverdraft(RuntimeError):
    ...


class LoanAlreadyDone(RuntimeError):
    ...


class LoanBeingPayed(RuntimeError):
    ...


class DataNotFound(RuntimeError):
    ...


class ImplicitAccType(RuntimeError):
    ...


class PayTooMuch(RuntimeError):
    ...


class InformationNotEnough(RuntimeError):
    ...


class AccountNotExists(RuntimeError):
    ...


class LoginExpired(RuntimeError):
    ...
