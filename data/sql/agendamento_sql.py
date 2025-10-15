CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS agendamento (
cod_agendamento INTEGER PRIMARY KEY AUTOINCREMENT,
cod_colaborador INTEGER,
cod_doador INTEGER NOT NULL,
data_hora TEXT NOT NULL,
status INTEGER NOT NULL,
tipo_agendamento TEXT NOT NULL,
local_agendamento INTEGER NOT NULL,
FOREIGN KEY (cod_colaborador) REFERENCES colaborador(cod_colaborador),
FOREIGN KEY (cod_doador) REFERENCES doador(cod_doador),
FOREIGN KEY (local_agendamento) REFERENCES unidade_coleta(cod_unidade)
)
"""

INSERIR = """
INSERT INTO agendamento (cod_colaborador, cod_doador, data_hora, status, tipo_agendamento, local_agendamento) 
VALUES (?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT a.cod_agendamento, a.cod_colaborador, d.cod_doador, a.data_hora, a.status, a.tipo_agendamento, a.local_agendamento
FROM agendamento a
INNER JOIN doador d ON a.cod_doador = d.cod_doador
INNER JOIN unidade_coleta u ON a.local_agendamento = u.cod_unidade
LEFT JOIN colaborador c ON a.cod_colaborador = c.cod_colaborador
""" 

UPDATE = """
UPDATE agendamento
SET data_hora = ?, status = ?, tipo_agendamento = ?
WHERE cod_agendamento = ?;
"""

DELETE = """
DELETE FROM agendamento
WHERE cod_agendamento = ?;
"""

OBTER_POR_ID = """
SELECT a.cod_agendamento, a.cod_colaborador, d.cod_doador, a.data_hora, a.status, a.tipo_agendamento, a.local_agendamento
FROM agendamento a
INNER JOIN doador d ON a.cod_doador = d.cod_doador
INNER JOIN unidade_coleta u ON a.local_agendamento = u.cod_unidade
LEFT JOIN colaborador c ON a.cod_colaborador = c.cod_colaborador
WHERE a.cod_agendamento = ?;
"""