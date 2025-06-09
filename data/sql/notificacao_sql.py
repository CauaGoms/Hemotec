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
SELECT 
cod_notificacao, cod_adm, destino, tipo, mensagem, status, data_envio
FROM notificacao
""" 