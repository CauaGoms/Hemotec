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
INSERT INTO adm_campanha (cod_adm, cod_campanha, papel) 
VALUES (?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
cod_adm, cod_campanha, papel
FROM adm_campanha
""" 