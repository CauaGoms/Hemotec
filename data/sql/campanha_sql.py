CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS campanha (
cod_campanha INTEGER PRIMARY KEY AUTOINCREMENT,
titulo TEXT NOT NULL,
descricao TEXT NOT NULL,
data_inicio DATE NOT NULL,
data_fim DATE NOT NULL,
status TEXT NOT NULL
)
"""

INSERIR = """
INSERT INTO campanha (titulo, descricao, data_inicio, data_fim, status) 
VALUES (?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
cod_campanha, titulo, descricao, data_inicio, data_fim, status
FROM campanha
""" 