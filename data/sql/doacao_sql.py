CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS doacao (
cod_doacao INTEGER PRIMARY KEY AUTOINCREMENT,
cod_doador INTEGER NOT NULL,
cod_exame INTEGER NOT NULL,
data_hora TEXT NOT NULL,
quantidade INTEGER NOT NULL,
status INTEGER NOT NULL,
FOREIGN KEY (cod_doador) REFERENCES doador(cod_doador),
FOREIGN KEY (cod_exame) REFERENCES exame(cod_exame)
)
"""

INSERIR = """
INSERT INTO doacao (cod_doador, cod_exame, data_hora, quantidade, status) 
VALUES (?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT d.cod_doacao, o.cod_doador, e.cod_exame, d.data_hora, d.quantidade, d.status
FROM doacao d,
doador o,
exame e
WHERE d.cod_doador = o.cod_doador
AND d.cod_exame = e.cod_exame
""" 

UPDATE = """
UPDATE cod_doacao, cod_doador, cod_exame, data_hora, quantidade, status
SET cod_doador = ?, cod_exame = ?, data_hora = ?, quantidade = ?, status = ?
WHERE cod_doacao = ?;
"""

DELETE = """
DELETE FROM doacao
WHERE cod_doacao = ?;
"""

OBTER_POR_ID = """
SELECT d.cod_doacao, o.cod_doador, e.cod_exame, d.data_hora, d.quantidade, d.status
FROM doacao d,
doador o,
exame e
WHERE d.cod_doador = o.cod_doador
AND d.cod_exame = e.cod_exame
AND d.cod_doacao = ?;
"""