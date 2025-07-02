CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS licenca (
cod_licenca INTEGER PRIMARY KEY AUTOINCREMENT,
cod_assinatura INTEGER NOT NULL,
status INTEGER NOT NULL,
FOREIGN KEY (cod_assinatura) REFERENCES assinatura(cod_assinatura)
)
"""

INSERIR = """
INSERT INTO licenca (cod_assinatura, status)
VALUES (?, ?)
""" 

OBTER_TODOS = """
SELECT l.cod_licenca, a.cod_assinatura, l.status
FROM licenca l,
assinatura a
WHERE l.cod_assinatura = a.cod_assinatura
""" 

UPDATE = """
UPDATE licenca
SET cod_assinatura = ?, status = ?
WHERE cod_licenca = ?;
"""

DELETE = """
DELETE FROM licenca
WHERE cod_licenca = ?;
"""

OBTER_POR_ID = """
SELECT l.cod_licenca, a.cod_assinatura, l.status
FROM licenca l,
assinatura a
WHERE l.cod_assinatura = a.cod_assinatura
AND l.cod_licenca = ?;
"""