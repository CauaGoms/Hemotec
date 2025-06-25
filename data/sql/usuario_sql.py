CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS usuario (
cod_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL,
email TEXT NOT NULL UNIQUE,
senha TEXT NOT NULL,
cpf TEXT NOT NULL,
data_nascimento TEXT NOT NULL,
status INTEGER NOT NULL,
data_cadastro TEXT NOT NULL,
rua_usuario TEXT NOT NULL, 
bairro_usuario TEXT NOT NULL,
cidade_usuario INTEGER NOT NULL,
cep_usuario TEXT NOT NULL,
telefone TEXT NOT NULL,
FOREIGN KEY (cidade_usuario) REFERENCES cidade(cod_cidade)
)
"""

INSERIR = """
INSERT INTO usuario (nome, email, senha, cpf, data_nascimento, status, data_cadastro, rua_usuario, bairro_usuario, cidade_usuario, cep_usuario, telefone) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT u.cod_usuario, u.nome, u.email, u.senha, u.cpf, u.data_nascimento, u.status, u.data_cadastro, u.rua_usuario, u.bairro_usuario, c.cod_cidade, u.cep_usuario, u.telefone
FROM usuario u,
cidade c
WHERE u.cidade_usuario = c.cod_cidade
""" 

UPDATE = """
UPDATE usuario
SET nome = ?, email = ?, senha = ?, cpf = ?, data_nascimento = ?, status = ?, data_cadastro = ?, rua_usuario = ?, bairro_usuario = ?, cidade_usuario = ?, cep_usuario = ?, telefone = ?
WHERE cod_usuario = ?;
"""

ALTERAR_SENHA = """
UPDATE usuario
SET senha = ?
WHERE cod_usuario = ?;
"""

DELETE = """
DELETE FROM usuario
WHERE cod_usuario = ?;
"""

OBTER_POR_ID = """
SELECT u.cod_usuario, u.nome, u.email, u.senha, u.cpf, u.data_nascimento, u.status, u.data_cadastro, u.rua_usuario, u.bairro_usuario, c.cod_cidade, u.cep_usuario, u.telefone
FROM usuario u,
cidade c
WHERE u.cidade_usuario = c.cod_cidade
AND u.cod_usuario = ?;
"""

OBTER_POR_EMAIL = """
SELECT u.cod_usuario, u.nome, u.email, u.senha, u.cpf, u.data_nascimento, u.status, u.data_cadastro, u.rua_usuario, u.bairro_usuario, u.cidade_usuario, u.cep_usuario, u.telefone
FROM usuario u,
cidade c
WHERE u.cidade_usuario = c.cod_cidade
AND u.email = ?;
"""