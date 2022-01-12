import pandas as pd
from utils.utils import select_all

def get_key_list(cursor, insert_table):

    columns, data = select_all(cursor, insert_table)
    df = pd.DataFrame(data, columns=columns)

    return df['run_date']


def get_method(row, keys):

    if row['start_date'] in str(keys):
        return 'update'
    return 'insert'


def insert_record(conn, table, date, miles):

    local_cursor = conn.cursor()

    insert_query = "INSERT INTO " + table + " (run_date, miles) VALUES ('" + date + "', " + str(miles) + ")"
    local_cursor.execute(insert_query)
    conn.commit()

    local_cursor.close()


def update_record(conn, table, date, miles):

    local_cursor = conn.cursor()

    update_query = "UPDATE " + table + " SET miles = " + str(miles) + " WHERE run_date = '" + date + "'"
    local_cursor.execute(update_query)
    conn.commit()

    local_cursor.close()


def update_database(conn, data, insert_table):

    local_cursor = conn.cursor()

    keys = get_key_list(local_cursor, insert_table)

    for index, row in data.iterrows():
        method = get_method(row, keys)

        if method == 'insert':
            insert_record(conn, insert_table, row['start_date'], row['miles'])
        elif method == 'update':
            update_record(conn, insert_table, row['start_date'], row['miles'])


