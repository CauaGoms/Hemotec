"""
Migration: Adiciona campos de verificação de email na tabela usuario
"""
import sqlite3
from pathlib import Path

def migrate():
    db_path = Path(__file__).parent / "dados.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Adicionar campo email_verificado (padrão False/0)
        cursor.execute("""
            ALTER TABLE usuario 
            ADD COLUMN email_verificado INTEGER DEFAULT 0
        """)
        print("✓ Campo email_verificado adicionado")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("⚠ Campo email_verificado já existe")
        else:
            raise
    
    try:
        # Adicionar campo codigo_verificacao
        cursor.execute("""
            ALTER TABLE usuario 
            ADD COLUMN codigo_verificacao TEXT
        """)
        print("✓ Campo codigo_verificacao adicionado")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("⚠ Campo codigo_verificacao já existe")
        else:
            raise
    
    try:
        # Adicionar campo data_codigo_verificacao
        cursor.execute("""
            ALTER TABLE usuario 
            ADD COLUMN data_codigo_verificacao TIMESTAMP
        """)
        print("✓ Campo data_codigo_verificacao adicionado")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("⚠ Campo data_codigo_verificacao já existe")
        else:
            raise
    
    conn.commit()
    conn.close()
    
    print("\n✅ Migration concluída com sucesso!")

if __name__ == "__main__":
    migrate()
