CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS estoque (
cod_estoque INTEGER PRIMARY KEY AUTOINCREMENT,
cod_unidade INTEGER NOT NULL,
tipo_sanguineo TEXT NOT NULL,
fator_rh TEXT NOT NULL,
quantidade INTEGER NOT NULL,
data_atualizacao TEXT NOT NULL,
FOREIGN KEY (cod_unidade) REFERENCES unidade_coleta(cod_unidade)
)
"""

INSERIR = """
INSERT INTO estoque (cod_unidade, tipo_sanguineo, fator_rh, quantidade, data_atualizacao) 
VALUES (?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT e.cod_estoque, u.cod_unidade, e.tipo_sanguineo, e.fator_rh, e.quantidade, e.data_atualizacao
FROM estoque e,
unidade_coleta u
WHERE e.cod_unidade = u.cod_unidade
""" 

UPDATE = """
UPDATE estoque
SET cod_unidade = ?, tipo_sanguineo = ?, fator_rh = ?, quantidade = ?, data_atualizacao = ?
WHERE cod_estoque = ?;
"""

DELETE = """
DELETE FROM estoque
WHERE cod_estoque = ?;
"""

OBTER_POR_ID = """
SELECT e.cod_estoque, u.cod_unidade, e.tipo_sanguineo, e.fator_rh, e.quantidade, e.data_atualizacao
FROM estoque e,
unidade_coleta u
WHERE e.cod_unidade = u.cod_unidade
AND e.cod_estoque = ?;
"""