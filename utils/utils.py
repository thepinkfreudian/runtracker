import sys
import json
from datetime import datetime


def exit_on_error(error_message):

    print(error_message)
    sys.exit(1)


def validate_input_date(date):
    try:
        dt = datetime.strptime(date + ' 00:00:00,76', '%m/%d/%Y %H:%M:%S,%f')
        return True
    except ValueError:
        return False


def validate_environment(environment):
    if environment not in ['dev', 'prod']:
        return False
    return True


def get_session_config(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)

    return config


def select_all(cursor, table):
    cols_query = 'SHOW COLUMNS FROM ' + table
    data_query = 'SELECT * FROM ' + table

    cursor.execute(cols_query)
    cols = cursor.fetchall()
    columns = [col[0] for col in cols]

    cursor.execute(data_query)
    data = cursor.fetchall()

    return columns, data
