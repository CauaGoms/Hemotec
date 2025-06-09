CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS usuario (
cod_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL,
email TEXT NOT NULL,
senha TEXT NOT NULL,
cpf TEXT NOT NULL,
data_nascimento TEXT NOT NULL,
status INTEGER NOT NULL,
data_cadastro TEXT NOT NULL,
rua_usuario TEXT NOT NULL, 
bairro_usuario TEXT NOT NULL,
cidade_usuario INTEGER NOT NULL,
cep_usuario TEXT NOT NULL,
FOREIGN KEY (cidade_usuario) REFERENCES cidade(cod_cidade)
)
"""

INSERIR = """
INSERT INTO cliente (nome, email, senha, cpf, data_nascimento, status, data_cadastro, rua_usuario, bairro_usuario, cidade_usuario, cep_usuario) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
cod_usuario, nome, email, senha, cpf, data_nascimento, status, data_cadastro, rua_usuario, bairro_usuario, cidade_usuario, cep_usuario
FROM usuario
ORDER BY nome
""" 