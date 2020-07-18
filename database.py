#!/usr/bin/python


import sqlite3

DATABASE = 'database.db'


def connect_db():
    return sqlite3.connect(DATABASE)


def run_sql_script(filename, connection):
    sql = open(filename, 'r')

    cursor = connection.cursor()
    cursor.executescript(sql.read())
    connection.commit()
    connection.close()


def main():
    run_sql_script("schema.sql", connect_db())
    print("DATABASE SCHEMA SET UP!")
    run_sql_script("populate_db.sql", connect_db())
    print("DATABASE POPULATED!")


if __name__ == "__main__":
    main()