CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS doador (
cod_doador INTEGER PRIMARY KEY FOREIGN KEY AUTOINCREMENT,
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
SELECT 
cod_doador, cod_doacao, cod_agendamento, tipo_sanguineo, fator_rh, elegivel
FROM doador
""" 