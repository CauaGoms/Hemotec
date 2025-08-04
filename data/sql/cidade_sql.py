CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS cidade (
cod_cidade INTEGER PRIMARY KEY AUTOINCREMENT,
nome_cidade TEXT NOT NULL,
sigla_estado TEXT NOT NULL
)
"""

INSERIR = """
INSERT INTO cidade (nome_cidade, sigla_estado) 
VALUES (?, ?)
"""

OBTER_TODOS = """
SELECT c.cod_cidade, c.nome_cidade, c.sigla_estado
FROM cidade c
""" 

UPDATE = """
UPDATE cidade
SET nome_cidade = ?, sigla_estado = ?
WHERE cod_cidade = ?;
"""

DELETE = """
DELETE FROM cidade
WHERE cod_cidade = ?;
"""

OBTER_POR_ID = """
SELECT c.cod_cidade, c.nome_cidade, c.sigla_estado
FROM cidade c
WHERE c.cod_cidade = ?;
"""

OBTER_POR_NOME = """
SELECT c.cod_cidade, c.nome_cidade, c.sigla_estado
FROM cidade c
WHERE c.nome_cidade = ?;
"""