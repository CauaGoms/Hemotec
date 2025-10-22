CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS agenda (
cod_agenda INTEGER PRIMARY KEY AUTOINCREMENT,
cod_unidade INTEGER NOT NULL,
cod_agendamento INTEGER,
data_agenda DATE NOT NULL,
hora_agenda TIME NOT NULL,
vagas INTEGER NOT NULL,
quantidade_doadores INTEGER NOT NULL DEFAULT 0,
FOREIGN KEY (cod_unidade) REFERENCES unidade_coleta(cod_unidade),
FOREIGN KEY (cod_agendamento) REFERENCES agendamento(cod_agendamento)
)
"""

INSERIR = """
INSERT INTO agenda (cod_unidade, cod_agendamento, data_agenda, hora_agenda, vagas, quantidade_doadores) 
VALUES (?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT a.cod_agenda, a.cod_unidade, a.cod_agendamento, a.data_agenda, a.hora_agenda, a.vagas, a.quantidade_doadores
FROM agenda a
INNER JOIN unidade_coleta u ON a.cod_unidade = u.cod_unidade
LEFT JOIN agendamento ag ON a.cod_agendamento = ag.cod_agendamento
""" 

UPDATE = """
UPDATE agenda
SET cod_unidade = ?, cod_agendamento = ?, data_agenda = ?, hora_agenda = ?, vagas = ?, quantidade_doadores = ?
WHERE cod_agenda = ?;
"""

DELETE = """
DELETE FROM agenda
WHERE cod_agenda = ?;
"""

OBTER_POR_ID = """
SELECT a.cod_agenda, a.cod_unidade, a.cod_agendamento, a.data_agenda, a.hora_agenda, a.vagas, a.quantidade_doadores
FROM agenda a
INNER JOIN unidade_coleta u ON a.cod_unidade = u.cod_unidade
LEFT JOIN agendamento ag ON a.cod_agendamento = ag.cod_agendamento
WHERE a.cod_agenda = ?;
"""

OBTER_POR_UNIDADE = """
SELECT a.cod_agenda, a.cod_unidade, a.cod_agendamento, a.data_agenda, a.hora_agenda, a.vagas, a.quantidade_doadores
FROM agenda a
WHERE a.cod_unidade = ?
ORDER BY a.data_agenda, a.hora_agenda;
"""

OBTER_POR_DATA = """
SELECT a.cod_agenda, a.cod_unidade, a.cod_agendamento, a.data_agenda, a.hora_agenda, a.vagas, a.quantidade_doadores
FROM agenda a
INNER JOIN unidade_coleta u ON a.cod_unidade = u.cod_unidade
LEFT JOIN agendamento ag ON a.cod_agendamento = ag.cod_agendamento
WHERE a.data_agenda = ?
ORDER BY a.hora_agenda;
"""

OBTER_POR_UNIDADE_E_DATA = """
SELECT a.cod_agenda, a.cod_unidade, a.cod_agendamento, a.data_agenda, a.hora_agenda, a.vagas, a.quantidade_doadores
FROM agenda a
WHERE a.cod_unidade = ? AND a.data_agenda = ?
ORDER BY a.hora_agenda;
"""

INCREMENTAR_DOADORES = """
UPDATE agenda
SET quantidade_doadores = quantidade_doadores + 1
WHERE cod_agenda = ?;
"""

DECREMENTAR_DOADORES = """
UPDATE agenda
SET quantidade_doadores = quantidade_doadores - 1
WHERE cod_agenda = ? AND quantidade_doadores > 0;
"""

OBTER_VAGAS_DISPONIVEIS = """
SELECT (a.vagas - a.quantidade_doadores) as vagas_disponiveis
FROM agenda a
WHERE a.cod_agenda = ?;
"""

OBTER_POR_UNIDADE_DATA_HORA = """
SELECT a.cod_agenda, a.cod_unidade, a.cod_agendamento, a.data_agenda, a.hora_agenda, a.vagas, a.quantidade_doadores
FROM agenda a
WHERE a.cod_unidade = ? AND a.data_agenda = ? AND a.hora_agenda = ?;
"""
