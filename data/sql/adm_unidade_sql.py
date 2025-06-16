CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS adm_unidade (
cod_adm INTEGER PRIMARY KEY NOT NULL,
cod_unidade INTEGER NOT NULL,
cod_notificacao INTEGER NOT NULL,
permissao_envio_campanha BOOLEAN NOT NULL,
permissao_envio_notificacao BOOLEAN NOT NULL,
FOREIGN KEY (cod_adm) REFERENCES usuario(cod_usuario),
FOREIGN KEY (cod_unidade) REFERENCES unidade(cod_unidade),
FOREIGN KEY (cod_notificacao) REFERENCES notificacao(cod_notificacao)
)
"""

INSERIR = """
INSERT INTO adm_unidade (cod_adm, cod_unidade, cod_notificacao, permissao_envio_campanha, permissao_envio_notificacao) 
VALUES (?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
cod_adm, cod_unidade, cod_notificacao, permissao_envio_campanha, permissao_envio_notificacao
FROM adm_unidade
""" 

UPDATE = """
UPDATE cod_adm, cod_unidade, cod_notificacao, permissao_envio_campanha, permissao_envio_notificacao
SET cod_unidade = ?, cod_notificacao = ?, permissao_envio_campanha = ?, permissao_envio_notificacao = ?
WHERE cod_adm = ?;
"""

DELETE = """
DELETE FROM adm_unidade
WHERE cod_adm = ?;
"""

OBTER_POR_ID = """
SELECT usu.cod_adm, u.cod_unidade, n.cod_notificacao, adm.permissao_envio_campanha, adm.permissao_envio_notificacao
FROM adm_unidade adm,
unidade u,
notificacao n,
usuario usu
WHERE adm.cod_adm = usu.cod_usuario
AND adm.cod_unidade = u.cod_unidade
AND adm.cod_notificacao = n.cod_notificacao
AND adm.cod_adm = ?;
"""