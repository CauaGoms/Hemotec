CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS cidade (
cod_estado INTEGER PRIMARY KEY AUTOINCREMENT,
nome_cidade TEXT NOT NULL,
sigla_estado TEXT NOT NULL
)
"""

INSERIR = """
INSERT INTO cidade (nome_cidade, sigla_estado) 
VALUES (?, ?)
"""

OBTER_TODOS = """
SELECT 
cod_estado, nome_cidade, sigla_estado
FROM cidade
""" 

UPDATE = """
UPDATE cod_estado, nome_cidade, sigla_estado
SET nome_cidade = ?, sigla_estado = ?
WHERE cod_cidade = ?;
"""

DELETE = """
DELETE FROM cidade
WHERE cod_cidade = ?;
"""

OBTER_POR_ID = """
SELECT c.cod_estado, c.nome_cidade, c.sigla_estado
FROM cidade c
WHERE c.cod_cidade = ?;
"""