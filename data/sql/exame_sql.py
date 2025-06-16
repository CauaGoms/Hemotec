CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS exame (
cod_exame INTEGER PRIMARY KEY AUTOINCREMENT,
cod_doacao INTEGER NOT NULL,
data_exame TEXT NOT NULL,
tipo_exame TEXT NOT NULL,
resultado TEXT NOT NULL,
arquivo TEXT NOT NULL,
FOREIGN KEY (cod_doacao) REFERENCES doacao(cod_doacao)
)
"""

INSERIR = """
INSERT INTO exame (cod_doacao, data_exame, tipo_exame, resultado, arquivo) 
VALUES (?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
cod_exame, cod_doacao, data_exame, tipo_exame, resultado, arquivo
FROM exame
""" 

UPDATE = """
UPDATE cod_exame, cod_doacao, data_exame, tipo_exame, resultado, arquivo
SET cod_doacao = ?, data_exame = ?, tipo_exame = ?, resultado = ?, arquivo = ?
WHERE cod_exame = ?;
"""

DELETE = """
DELETE FROM exame
WHERE cod_exame = ?;
"""

OBTER_POR_ID = """
SELECT e.cod_exame, d.cod_doacao, e.data_exame, e.tipo_exame, e.resultado, e.arquivo
FROM exame e,
doacao d
WHERE e.cod_doacao = d.cod_doacao
AND e.cod_exame = ?;
"""