import sqlite3


class EasySQLite3:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self, path):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        self.conn.close()

    def insert_into(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    def select(self, query, fetch='one'):
        data = self.cursor.execute(query)
        if fetch == 'one':
            return data.fetchone()
        elif fetch == 'all':
            return data.fetchall()

    def update(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    def delete(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    def check_value(self, query):
        data = self.cursor.execute(query).fetchone()
        return data is not None
    
    def create_table(self, query):
        self.cursor.execute(query)
        self.conn.commit()
