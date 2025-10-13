CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS notificacao (
cod_notificacao INTEGER PRIMARY KEY AUTOINCREMENT,
cod_adm INTEGER NOT NULL,
tipo TEXT NOT NULL,
mensagem TEXT NOT NULL,
status INTEGER NOT NULL,
data_envio TEXT NOT NULL,
titulo TEXT NOT NULL,
FOREIGN KEY (cod_adm) REFERENCES adm_unidade(cod_adm)
)
"""

INSERIR = """
INSERT INTO notificacao (cod_adm, tipo, mensagem, status, data_envio, titulo)
VALUES (?, ?, ?, ?, ?, ?)
""" 

OBTER_TODOS = """
SELECT n.cod_notificacao, a.cod_adm, n.tipo, n.mensagem, n.status, n.data_envio, n.titulo
FROM notificacao n,
adm_unidade a
WHERE n.cod_adm = a.cod_adm
""" 

UPDATE = """
UPDATE notificacao
SET cod_adm = ?, tipo = ?, mensagem = ?, status = ?, data_envio = ?, titulo = ?
WHERE cod_notificacao = ?;
"""

DELETE = """
DELETE FROM notificacao
WHERE cod_notificacao = ?;
"""

OBTER_POR_ID = """
SELECT n.cod_notificacao, a.cod_adm, n.tipo, n.mensagem, n.status, n.data_envio, n.titulo
FROM notificacao n,
adm_unidade a
WHERE n.cod_adm = a.cod_adm
AND n.cod_notificacao = ?;
"""

CONTAR_NAO_LIDAS = """
SELECT COUNT(*) as total
FROM notificacao
WHERE status = 1;
"""

OBTER_ULTIMAS_NAO_LIDAS = """
SELECT n.cod_notificacao, a.cod_adm, n.tipo, n.mensagem, n.status, n.data_envio, n.titulo
FROM notificacao n,
adm_unidade a
WHERE n.cod_adm = a.cod_adm
AND n.status = 1
ORDER BY n.data_envio DESC
LIMIT ?;
"""