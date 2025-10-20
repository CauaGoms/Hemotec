import sqlite3
from passlib.context import CryptContext

# Hash da senha #Colaborador123
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
senha_hash = pwd_context.hash("#Colaborador123")

conn = sqlite3.connect('dados.db')
cur = conn.cursor()

# Inserir novo colaborador
try:
    cur.execute("""
        INSERT INTO usuario (nome, email, senha, cpf, data_nascimento, status, 
                           rua_usuario, bairro_usuario, cidade_usuario, cep_usuario, 
                           telefone, perfil, genero, data_cadastro, foto, 
                           token_redefinicao, data_token, estado_usuario)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        'Colaborador Test',
        'colaborador@gmail.com',
        senha_hash,
        '12345678999',
        '1990-01-01',
        1,  # status ativo
        'Rua Teste',
        'Bairro Teste',
        1,  # cidade id
        '29000000',
        '28999999999',
        'colaborador',
        'Masculino',
        '2025-10-20',
        '',
        '',
        '',
        'ES'
    ))
    
    conn.commit()
    print("✓ Usuário colaborador@gmail.com criado com sucesso!")
    print(f"Senha hash: {senha_hash}")
    
    # Verificar inserção
    cur.execute("SELECT cod_usuario, nome, email, perfil FROM usuario WHERE email='colaborador@gmail.com'")
    result = cur.fetchone()
    if result:
        print(f"Verificação: {result}")
    
except Exception as e:
    print(f"✗ Erro ao inserir: {e}")
finally:
    conn.close()
