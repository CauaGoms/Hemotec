CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS instituicao (
cnpj TEXT PRIMARY KEY NOT NULL, 
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
SELECT i.cnpj, i.nome, i.email, i.rua_instituicao, i.bairro_instituicao, c.cidade_instituicao, i.cep_instituicao, i.telefone
FROM instituicao i,
cidade c
WHERE i.cidade_instituicao = c.cod_cidade
"""

UPDATE = """
UPDATE instituicao
SET nome = ?, email = ?, rua_instituicao = ?, bairro_instituicao = ?, cidade_instituicao = ?, cep_instituicao = ?, telefone = ?
WHERE cnpj = ?;
"""

DELETE = """
DELETE FROM instituicao
WHERE cnpj = ?;
"""

OBTER_POR_ID = """
SELECT i.cnpj, i.nome, i.email, i.rua_instituicao, i.bairro_instituicao, c.cidade_instituicao, i.cep_instituicao, i.telefone
FROM instituicao i,
cidade c
WHERE i.cidade_instituicao = c.cod_cidade
AND i.cnpj = ?;
"""