CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS colaborador (
cod_colaborador INTEGER PRIMARY KEY AUTOINCREMENT,
cod_agendamento INTEGER NOT NULL,
funcao TEXT NOT NULL,
FOREIGN KEY (cod_colaborador) REFERENCES usuario(cod_usuario),
FOREIGN KEY (cod_agendamento) REFERENCES agendamento(cod_agendamento)
)
"""

INSERIR = """
INSERT INTO colaborador (cod_colaborador, cod_agendamento, funcao) 
VALUES (?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
cod_colaborador, cod_agendamento, funcao
FROM colaborador
""" 

UPDATE = """
UPDATE cod_colaborador, cod_agendamento, funcao
SET cod_agendamento = ?, funcao = ?
WHERE cod_colaborador = ?;
"""

DELETE = """
DELETE FROM colaborador
WHERE cod_colaborador = ?;
"""

OBTER_POR_ID = """
SELECT u.cod_colaborador, a.cod_agendamento, c.funcao
FROM colaborador c,
usuario u,
agendamento a
WHERE c.cod_colaborador = u.cod_usuario
AND c.cod_agendamento = a.cod_agendamento
WHERE c.cod_colaborador = ?;
"""