CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS plano (
cod_plano INTEGER PRIMARY KEY AUTOINCREMENT, 
qtd_licenca INTEGER NOT NULL,
nome TEXT NOT NULL,
valor REAL NOT NULL,
validade INTEGER NOT NULL
)
"""

INSERIR = """
INSERT INTO plano (qtd_licenca, nome, valor, validade) 
VALUES (?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT p.cod_plano, p.qtd_licenca, p.nome, p.valor, p.validade
FROM plano p
""" 

UPDATE = """
UPDATE plano
SET qtd_licenca = ?, nome = ?, valor = ?, validade = ?
WHERE cod_plano = ?;
"""

DELETE = """
DELETE FROM plano
WHERE cod_plano = ?;
"""

OBTER_POR_ID = """
SELECT p.cod_plano, p.qtd_licenca, p.nome, p.valor, p.validade
FROM plano p
WHERE p.cod_plano = ?;
"""