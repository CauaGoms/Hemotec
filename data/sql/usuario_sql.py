CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS usuario (
cod_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL,
email TEXT NOT NULL UNIQUE,
senha TEXT NOT NULL,
cpf TEXT NOT NULL,
data_nascimento TEXT NOT NULL,
status INTEGER NOT NULL,
rua_usuario TEXT NOT NULL, 
bairro_usuario TEXT NOT NULL,
cidade_usuario INTEGER NOT NULL,
cep_usuario TEXT NOT NULL,
telefone TEXT NOT NULL,
perfil TEXT NOT NULL DEFAULT 'doador',
data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
foto TEXT,
token_redefinicao TEXT,
data_token TIMESTAMP,
estado_usuario TEXT,
FOREIGN KEY (cidade_usuario) REFERENCES cidade(cod_cidade)
)
"""

INSERIR = """
INSERT INTO usuario (nome, email, senha, cpf, data_nascimento, status, rua_usuario, bairro_usuario, cidade_usuario, cep_usuario, telefone, perfil, data_cadastro, estado_usuario) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT u.cod_usuario, u.nome, u.email, u.senha, u.cpf, u.data_nascimento, u.status, u.rua_usuario, u.bairro_usuario, u.cidade_usuario, u.cep_usuario, u.telefone, u.perfil, u.data_cadastro, u.foto, u.estado_usuario
FROM usuario u,
cidade c
WHERE u.cidade_usuario = c.cod_cidade
""" 

UPDATE = """
UPDATE usuario
SET nome = ?, email = ?, senha = ?, cpf = ?, data_nascimento = ?, status = ?, rua_usuario = ?, bairro_usuario = ?, cidade_usuario = ?, cep_usuario = ?, telefone = ?, perfil = ?, estado_usuario = ?
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
SELECT u.cod_usuario, u.nome, u.email, u.senha, u.cpf, u.data_nascimento, u.status, u.rua_usuario, u.bairro_usuario, u.cidade_usuario, u.cep_usuario, u.telefone, u.perfil, u.data_cadastro, u.foto, u.token_redefinicao, u.data_token, u.estado_usuario
FROM usuario u,
cidade c
WHERE u.cidade_usuario = c.cod_cidade
AND u.cod_usuario = ?;
"""

OBTER_POR_EMAIL = """
SELECT u.cod_usuario, u.nome, u.email, u.senha, u.cpf, u.data_nascimento, u.status, u.rua_usuario, u.bairro_usuario, u.cidade_usuario, u.cep_usuario, u.telefone, u.perfil, u.data_cadastro, u.foto, u.estado_usuario
FROM usuario u,
cidade c
WHERE u.cidade_usuario = c.cod_cidade
AND u.email = ?;
"""

ATUALIZAR_TOKEN = """
UPDATE usuario
SET token_redefinicao=?, data_token=?
WHERE email=?
"""

ATUALIZAR_FOTO = """
UPDATE usuario
SET foto=?
WHERE cod_usuario=?
"""

OBTER_POR_TOKEN = """
SELECT u.cod_usuario, u.nome, u.email, u.senha, u.cpf, u.data_nascimento, u.status, u.rua_usuario, u.bairro_usuario, u.cidade_usuario, u.cep_usuario, u.telefone, u.perfil, u.data_cadastro, u.foto, u.token_redefinicao, u.data_token, u.estado_usuario
FROM usuario u,
cidade c
WHERE u.cidade_usuario = c.cod_cidade
AND u.token_redefinicao=? AND u.data_token > datetime('now')
"""