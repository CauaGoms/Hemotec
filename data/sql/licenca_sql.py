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
SELECT 
cod_licenca, cod_assinatura, cod_unidade, status
FROM licenca
""" 