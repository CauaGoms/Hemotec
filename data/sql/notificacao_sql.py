CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS notificacao (
cod_notificacao INTEGER PRIMARY KEY AUTOINCREMENT,
cod_adm INTEGER NOT NULL,
destino TEXT NOT NULL,
tipo TEXT NOT NULL,
mensagem TEXT NOT NULL,
status INTEGER NOT NULL,
data_envio TEXT NOT NULL,
FOREIGN KEY (cod_adm) REFERENCES adm_unidade(cod_adm)
)
"""

INSERIR = """
INSERT INTO notificacao (cod_adm, destino, tipo, mensagem, status, data_envio)
VALUES (?, ?, ?, ?, ?, ?)
""" 

OBTER_TODOS = """
SELECT n.cod_notificacao, a.cod_adm, n.destino, n.tipo, n.mensagem, n.status, n.data_envio
FROM notificacao n,
adm_unidade a
WHERE n.cod_adm = a.cod_adm
""" 

UPDATE = """
UPDATE cod_notificacao, cod_adm, destino, tipo, mensagem, status, data_envio
SET cod_adm = ?, destino = ?, tipo = ?, mensagem = ?, status = ?, data_envio = ?
WHERE cod_notificacao = ?;
"""

DELETE = """
DELETE FROM notificacao
WHERE cod_notificacao = ?;
"""

OBTER_POR_ID = """
SELECT n.cod_notificacao, a.cod_adm, n.destino, n.tipo, n.mensagem, n.status, n.data_envio
FROM notificacao n,
adm_unidade a
WHERE n.cod_adm = a.cod_adm
AND n.cod_notificacao = ?;
"""