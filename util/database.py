import sqlite3
import os

def get_connection():
    database_path = os.environ.get('TEST_DATABASE_PATH', 'dados.db')
    conexao = sqlite3.connect(database_path)
    conexao.execute("PRAGMA foreign_keys = ON") 
    conexao.row_factory = sqlite3.Row
    return conexao