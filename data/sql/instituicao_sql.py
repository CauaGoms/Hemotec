CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS instituicao (
cod_instituicao INTEGER PRIMARY KEY AUTOINCREMENT,
cnpj TEXT NOT NULL, 
nome TEXT NOT NULL,
email TEXT NOT NULL, 
rua_instituicao TEXT NOT NULL, 
bairro_instituicao TEXT NOT NULL,
cidade_instituicao INTEGER NOT NULL,
cep_instituicao TEXT NOT NULL,
telefone TEXT NOT NULL,
FOREIGN KEY (cidade_instituicao) REFERENCES cidade(cod_cidade)
)
"""

INSERIR = """
INSERT INTO instituicao (cnpj, nome, email, rua_instituicao, bairro_instituicao, cidade_instituicao, cep_instituicao, telefone) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT i.cod_instituicao, i.cnpj, i.nome, i.email, i.rua_instituicao, i.bairro_instituicao, c.cidade_instituicao, i.cep_instituicao, i.telefone
FROM instituicao i,
cidade c
WHERE i.cidade_instituicao = c.cod_cidade
"""

UPDATE = """
UPDATE instituicao
SET cnpj = ?, nome = ?, email = ?, rua_instituicao = ?, bairro_instituicao = ?, cep_instituicao = ?, telefone = ?
WHERE cod_instituicao = ?;
"""

DELETE = """
DELETE FROM instituicao
WHERE cod_instituicao = ?;
"""

OBTER_POR_ID = """
SELECT i.cod_instituicao, i.cnpj, i.nome, i.email, i.rua_instituicao, i.bairro_instituicao, i.cidade_instituicao, i.cep_instituicao, i.telefone
FROM instituicao i,
cidade c
WHERE i.cidade_instituicao = c.cod_cidade
AND i.cod_instituicao = ?;
"""