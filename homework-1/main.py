"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
import pymysql
import csv


def main() -> None:
    conn_params = {
        "host": "localhost",
        "database": "north",
        "user": "root",
        "password": ""
    }

    user_input_lib: int = int(input("1) PostgreSQL\n2) MySql\n"))
    if user_input_lib not in (1, 2):
        raise Exception('Ошибка')

    data_from_cvs: dict = {
        'employees': read_cvs('employees_data.csv'),
        'customers': read_cvs('customers_data.csv'),
        'orders': read_cvs('orders_data.csv')
    }

    user_lib = psycopg2 if user_input_lib == 1 else pymysql
    with user_lib.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            for table_name, data in data_from_cvs.items():
                formatted_tuple = tuple('%s' for _ in data[0])
                format_for_columns = ', '.join(formatted_tuple)
                cur.executemany(f"INSERT INTO {table_name} VALUES ({format_for_columns})", data)
            conn.commit()

    print('Таблицы заполнены')


def read_cvs(filename) -> list:
    table_row: list = []

    with open(f'north_data/{filename}', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            found_row: tuple = tuple(int(value) if value.isdigit() else value for value in row)
            table_row.append(found_row)

    return table_row


if __name__ == '__main__':
    main()
