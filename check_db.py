import sqlite3

conn = sqlite3.connect('dados.db')
cur = conn.cursor()

# Verificar colaboradores
print("=== COLABORADORES ===")
cur.execute("SELECT cod_usuario, nome, email, perfil FROM usuario WHERE perfil='colaborador' LIMIT 5")
for row in cur.fetchall():
    print(row)

# Verificar doadores
print("\n=== DOADORES ===")
cur.execute("SELECT cod_usuario, nome, email, perfil FROM usuario WHERE perfil='doador' LIMIT 5")
for row in cur.fetchall():
    print(row)

# Verificar todos os usuários
print("\n=== TODOS OS USUÁRIOS ===")
cur.execute("SELECT cod_usuario, nome, email, perfil FROM usuario LIMIT 10")
for row in cur.fetchall():
    print(row)

conn.close()
