import sqlite3, os
DB = 'data/cookie_runners.db'
def init(): conn=sqlite3.connect(DB); conn.execute('CREATE TABLE IF NOT EXISTS sources (id INTEGER PRIMARY KEY, name TEXT, url TEXT)'); conn.commit(); conn.close()
