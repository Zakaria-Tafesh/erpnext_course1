import sys
import traceback
import mariadb
from decouple import config


def connect_db():
    try:
        conn = mariadb.connect(
            user=config('DB_USER'),
            password=config('DB_PASSWORD'),
            host=config('DB_HOST'),
            port=int(config('DB_PORT')),
            database=config('DB_SCHEMA')

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    cur = conn.cursor()
    return cur, conn


def insert(table: str, data_dict: dict):
    cur, conn = connect_db()

    def close_conn():
        if conn:
            conn.close()
            print('MariaDb Connection Closed')

    try:
        statement = f"INSERT INTO {table} (%COLUMNS%) VALUES (%VALUES%)"

        columns_str = ','.join(data_dict.keys())
        print(columns_str)
        statement = statement.replace('%COLUMNS%', columns_str)
        print(statement)
        values_str = ('?,' * len(data_dict.keys()))[:-1]
        statement = statement.replace('%VALUES%', values_str)
        print(statement)

        cur.execute(statement, tuple(data_dict.values()))
        print(f'Data inserted Successfully into : {table}')
        last_id = cur.lastrowid
        print('last_id', last_id)

        conn.commit()
        print('Committed')
        return last_id

    except:
        traceback.print_exc()

    finally:
        close_conn()


def select(statement, multi_row=False):
    cur, conn = connect_db()

    def close_conn():
        if conn:
            conn.close()
            print('MariaDb Connection Closed')

    try:

        print(statement)
        cur.execute(statement)
        if multi_row:
            data = cur.fetchall()
        else:
            data = cur.fetchone()

        print("Total number of rows in table: ", cur.rowcount)
        return data

    except:
        traceback.print_exc()

    finally:
        close_conn()
