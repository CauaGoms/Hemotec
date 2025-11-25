import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('dados.db')
cursor = conn.cursor()

try:
    # Tentar adicionar as colunas se elas não existirem
    cursor.execute("ALTER TABLE adm_unidade ADD COLUMN permissao_envio_campanha INTEGER DEFAULT 0")
    print("Coluna permissao_envio_campanha adicionada com sucesso!")
except sqlite3.OperationalError as e:
    print(f"Erro ao adicionar permissao_envio_campanha (pode já existir): {e}")

try:
    cursor.execute("ALTER TABLE adm_unidade ADD COLUMN permissao_envio_notificacao INTEGER DEFAULT 0")
    print("Coluna permissao_envio_notificacao adicionada com sucesso!")
except sqlite3.OperationalError as e:
    print(f"Erro ao adicionar permissao_envio_notificacao (pode já existir): {e}")

# Commit e fechar
conn.commit()
conn.close()

print("\nMigração concluída!")
