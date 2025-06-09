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
SELECT 
cod_doacao, cod_doador, cod_exame, data_hora, quantidade, status
FROM doacao
""" 