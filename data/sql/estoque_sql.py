CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS estoque (
cod_estoque INTEGER PRIMARY KEY AUTOINCREMENT,
cod_unidade INTEGER NOT NULL,
tipo_sanguineo TEXT NOT NULL,
fator_rh TEXT NOT NULL,
quantidade INTEGER NOT NULL,
data_atualizacao TEXT NOT NULL,
FOREIGN KEY (cod_unidade) REFERENCES unidade(cod_unidade)
)
"""

INSERIR = """
INSERT INTO estoque (cod_unidade, tipo_sanguineo, fator_rh, quantidade, data_atualizacao) 
VALUES (?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
cod_estoque, cod_unidade, tipo_sanguineo, fator_rh, quantidade, data_atualizacao
FROM estoque
""" 