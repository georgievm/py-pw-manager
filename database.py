import psycopg2
from settings import (
    DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT
)

db_config = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_NAME,
    'port': DB_PORT
}

class Database:
    def __init__(self):
        self._conn = psycopg2.connect(**db_config)
        self._cursor = self._conn.cursor()

    # Allows to use it like context manager
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()
        print('Bye!')

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        self.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()
    
    def add_record(self, url, username, encr_pw, nonce, auth_tag):
        sql = """
            INSERT INTO records (url, username, encr_pw, nonce, auth_tag)
            VALUES (%s, %s, %s, %s, %s);
        """
        self.execute(sql, (url, username, encr_pw, nonce, auth_tag))
        print('Added!')
    
    def del_record(self, record_id):
        sql = "DELETE from records WHERE record_id = %s;"
        self.execute(sql, (record_id,))
        print('Deleted!')
    
    def get_record(self, record_id):
        sql = "SELECT * FROM records WHERE record_id = %s;"
        self.execute(sql, (record_id,))
        
        return self.fetchone()
    
    def get_all(self):
        return self.query("SELECT * FROM records ORDER BY url;")

