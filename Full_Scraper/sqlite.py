import sqlite3
from sqlite3 import Error


def create_connection():
    try:
        conn = sqlite3.connect("sozcu.db")
        return conn
    except Error as e:
        print(e)


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_tables(conn):
    new_urls_table = """ CREATE TABLE IF NOT EXISTS new_urls (
                         url text NOT NULL
                         ); """

    processed_urls_table = """ CREATE TABLE IF NOT EXISTS processed_urls (
                               url text NOT NULL
                               ); """

    local_urls_table = """ CREATE TABLE IF NOT EXISTS local_urls (
                           url text NOT NULL
                           ); """

    foreign_urls_table = """ CREATE TABLE IF NOT EXISTS foreign_urls (
                             url text NOT NULL
                             ); """

    broken_urls_table = """ CREATE TABLE IF NOT EXISTS broken_urls (
                            url text NOT NULL
                            ); """

    keyword_urls_table = """ CREATE TABLE IF NOT EXISTS keyword_urls (
                             url text NOT NULL
                             ); """

    # create tables
    if conn is not None:
        # create tables
        create_table(conn, new_urls_table)
        create_table(conn, processed_urls_table)
        create_table(conn, local_urls_table)
        create_table(conn, foreign_urls_table)
        create_table(conn, broken_urls_table)
        create_table(conn, keyword_urls_table)
    else:
        print("Error! cannot create the database connection.")


def insert_row(conn, table, url):
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {table} (url) VALUES('{url}');")
    conn.commit()
    return cur.lastrowid


def insert_row_if_not_in(conn, table, url):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table} WHERE url = '{url}'")
    rows = cur.fetchall()
    if url not in [a[0] for a in rows]:
        cur.execute(f"INSERT INTO {table} (url) VALUES('{url}')")
        conn.commit()
    return cur.lastrowid


def select_all_rows(conn, table):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    return rows


def delete_row(conn, table, url):
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {table} WHERE url = '{url}'")
    conn.commit()


def main():
    conn = create_connection()
    create_tables(conn)
    conn.close()


if __name__ == '__main__':
    main()
