from pymysql.cursors import Cursor
from datetime import datetime

sql_datetime_format = '%Y-%m-%d %H:%M:%S'


def sql_str2datetime(string: str):
    return datetime.strptime(string, sql_datetime_format)


def sql_datetime2str(date: datetime):
    return date.strftime(sql_datetime_format)


def execute_sql(cursor: Cursor, path):
    with open(path, 'r') as f:
        for query in f.read().split(';'):
            query = query.strip('\r\n\t ')
            if query != '':
                cursor.execute(query)
