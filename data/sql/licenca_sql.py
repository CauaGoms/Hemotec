CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS licenca (
cod_licenca INTEGER PRIMARY KEY AUTOINCREMENT,
cod_assinatura INTEGER NOT NULL,
cod_unidade INTEGER NOT NULL, 
status INTEGER NOT NULL,
FOREIGN KEY (cod_assinatura) REFERENCES assinatura(cod_assinatura),
FOREIGN KEY (cod_unidade) REFERENCES unidade(cod_unidade)
)
"""

INSERIR = """
INSERT INTO licenca (cod_assinatura, cod_unidade, status)
VALUES (?, ?, ?)
""" 

OBTER_TODOS = """
SELECT l.cod_licenca, a.cod_assinatura, u.cod_unidade, l.status
FROM licenca l,
assinatura a,
unidade u
WHERE l.cod_assinatura = a.cod_assinatura
AND l.cod_unidade = u.cod_unidade
""" 

UPDATE = """
UPDATE cod_licenca, cod_assinatura, cod_unidade, status
SET cod_assinatura = ?, cod_unidade = ?, status = ?
WHERE cod_licenca = ?;
"""

DELETE = """
DELETE FROM licenca
WHERE cod_licenca = ?;
"""

OBTER_POR_ID = """
SELECT l.cod_licenca, a.cod_assinatura, u.cod_unidade, l.status
FROM licenca l,
assinatura a,
unidade u
WHERE l.cod_assinatura = a.cod_assinatura
AND l.cod_unidade = u.cod_unidade
AND l.cod_licenca = ?;
"""