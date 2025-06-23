CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS doador (
cod_doador INTEGER PRIMARY KEY AUTOINCREMENT,
cod_doacao INTEGER NOT NULL,
cod_agendamento INTEGER NOT NULL,
tipo_sanguineo TEXT NOT NULL,
fator_rh TEXT NOT NULL,
elegivel TEXT NOT NULL,
FOREIGN KEY (cod_doador) REFERENCES usuario(cod_usuario),
FOREIGN KEY (cod_doacao) REFERENCES doacao(cod_doacao),
FOREIGN KEY (cod_agendamento) REFERENCES agendamento(cod_agendamento)
)
"""

INSERIR = """
INSERT INTO doador (cod_doador, cod_doacao, cod_agendamento, tipo_sanguineo, fator_rh, elegivel) 
VALUES (?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT o.cod_doador, e.cod_doacao, a.cod_agendamento, d.tipo_sanguineo, d.fator_rh, d.elegivel
FROM doador d,
usuario o,
doacao e,
agendamento a
WHERE d.cod_doador = o.cod_usuario
AND d.cod_doacao = e.cod_doacao
AND d.cod_agendamento = a.cod_agendamento
""" 

UPDATE = """
UPDATE cod_doador, cod_doacao, cod_agendamento, tipo_sanguineo, fator_rh, elegivel
SET cod_doacao = ?, cod_agendamento = ?, tipo_sanguineo = ?, fator_rh = ?, elegivel = ?
WHERE cod_doador = ?;
"""

DELETE = """
DELETE FROM doador
WHERE cod_doador = ?;
"""

OBTER_POR_ID = """
SELECT o.cod_doador, e.cod_doacao, a.cod_agendamento, d.tipo_sanguineo, d.fator_rh, d.elegivel
FROM doador d,
usuario o,
doacao e,
agendamento a
WHERE d.cod_doador = o.cod_usuario
AND d.cod_doacao = e.cod_doacao
AND d.cod_agendamento = a.cod_agendamento
AND d.cod_doador = ?;
"""