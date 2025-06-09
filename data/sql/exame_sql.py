CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS exame (
cod_exame INTEGER PRIMARY KEY AUTOINCREMENT,
cod_doacao INTEGER NOT NULL,
data_exame TEXT NOT NULL,
tipo_exame TEXT NOT NULL,
resultado TEXT NOT NULL,
arquivo TEXT NOT NULL,
FOREIGN KEY (cod_doacao) REFERENCES doacao(cod_doacao)
)
"""

INSERIR = """
INSERT INTO exame (cod_doacao, data_exame, tipo_exame, resultado, arquivo) 
VALUES (?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
cod_exame, cod_doacao, data_exame, tipo_exame, resultado, arquivo
FROM exame
""" 