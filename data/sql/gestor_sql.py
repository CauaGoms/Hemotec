CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS gestor (
cod_gestor INTEGER PRIMARY KEY,
cnpj TEXT NOT NULL,
instituicao TEXT NOT NULL,
FOREIGN KEY (cod_gestor) REFERENCES usuario(cod_usuario),
FOREIGN KEY (cnpj) REFERENCES instituicao(cnpj)
)
"""

INSERIR = """
INSERT INTO gestor (cod_gestor, cnpj, instituicao) 
VALUES (?, ?, ?)
"""

OBTER_TODOS = """
SELECT u.cod_gestor, i.cnpj, g.instituicao
FROM gestor g,
usuario u,
instituicao i
WHERE g.cod_gestor = u.cod_usuario
AND g.cnpj = i.cnpj
""" 

UPDATE = """
UPDATE gestor
SET cnpj = ?, instituicao = ?
WHERE cod_gestor = ?;
"""

DELETE = """
DELETE FROM gestor
WHERE cod_gestor = ?;
"""

OBTER_POR_ID = """
SELECT u.cod_gestor, i.cnpj, g.instituicao
FROM gestor g,
usuario u,
instituicao i
WHERE g.cod_gestor = u.cod_usuario
AND g.cnpj = i.cnpj
AND g.cod_gestor = ?;
"""