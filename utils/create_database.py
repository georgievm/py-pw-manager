import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Credentials for connecting to Your PostgreSQL server
DB_HOST = 'localhost'
DB_USER = 'postgres'
DB_PW = 'password'


def close(conn, cursor):
    cursor.close()
    conn.close()


def create_database():
    try:
        conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PW)
    except Exception as e:
        print(f'Unable to connect to server!\n{e}')
    else:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE pw_manager;")
        print('Database Created!')

        close(conn, cursor)


def create_table():
    try:
        conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PW, database='pw_manager')
    except Exception as e:
        print(f'Unable to connect to database!\n{e}')
    else:
        cursor = conn.cursor()
        with conn:
            cursor.execute("""
                CREATE TABLE records (
                record_id SERIAL PRIMARY KEY,
                url text,
                username text,
                encr_pw bytea,
                nonce bytea,
                auth_tag bytea);
            """)
        print('Table Created!')

        close(conn, cursor)

create_database()
create_table()
