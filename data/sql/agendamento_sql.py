CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS agendamento (
cod_agendamento INTEGER PRIMARY KEY AUTOINCREMENT,
cod_colaborador INTEGER NOT NULL,
cod_doador INTEGER NOT NULL,
data_hora TEXT NOT NULL,
status INTEGER NOT NULL,
observacoes TEXT NOT NULL,
tipo_agendamento TEXT NOT NULL,
FOREIGN KEY (cod_colaborador) REFERENCES colaborador(cod_colaborador),
FOREIGN KEY (cod_doador) REFERENCES doador(cod_doador)
)
"""

INSERIR = """
INSERT INTO agendamento (cod_colaborador, cod_doador, data_hora, status, observacoes, tipo_agendamento) 
VALUES (?, ?, ?, ? , ?, ?)
"""

OBTER_TODOS = """
SELECT 
cod_agendamento, cod_colaborador, cod_doador, data_hora, status, observacoes, tipo_agendamento
FROM agendamento
""" 

UPDATE = """
UPDATE cod_agendamento, cod_colaborador, cod_doador, data_hora, status, observacoes, tipo_agendamento
SET cod_colaborador = ?, cod_doador = ?, data_hora = ?, status = ?, observacoes = ?, tipo_agendamento = ?
WHERE cod_agendamento = ?;
"""

DELETE = """
DELETE FROM agendamento
WHERE cod_agendamento = ?;
"""

OBTER_POR_ID = """
SELECT a.cod_agendamento, c.cod_colaborador, d.cod_doador, a.data_hora, a.status, a.observacoes, a.tipo_agendamento
FROM agendamento a,
colaborador c,
doador d
WHERE a.cod_colaborador = c.cod_colaborador
AND a.cod_doador = d.cod_doador
AND a.cod_agendamento = ?;
"""