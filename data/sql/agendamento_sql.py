CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS agendamento (
cod_agendamento INTEGER PRIMARY KEY NOT NULL AUTOINCREMENT,
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