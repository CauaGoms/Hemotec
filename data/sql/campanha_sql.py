CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS campanha (
cod_campanha INTEGER PRIMARY KEY AUTOINCREMENT,
titulo TEXT NOT NULL,
descricao TEXT NOT NULL,
data_inicio DATE NOT NULL,
data_fim DATE NOT NULL,
status TEXT NOT NULL,
foto TEXT
)
"""

INSERIR = """
INSERT INTO campanha (titulo, descricao, data_inicio, data_fim, status, foto) 
VALUES (?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT c.cod_campanha, c.titulo, c.descricao, c.data_inicio, c.data_fim, c.status, c.foto
FROM campanha c
""" 

UPDATE = """
UPDATE campanha
SET titulo = ?, descricao = ?, data_inicio = ?, data_fim = ?, status = ?, foto = ?
WHERE cod_campanha = ?;
"""

DELETE = """
DELETE FROM campanha
WHERE cod_campanha = ?;
"""

OBTER_POR_ID = """
SELECT c.cod_campanha, c.titulo, c.descricao, c.data_inicio, c.data_fim, c.status, c.foto
FROM campanha c
WHERE c.cod_campanha = ?;
"""