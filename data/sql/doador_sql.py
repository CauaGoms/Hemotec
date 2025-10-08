CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS doador (
cod_doador INTEGER PRIMARY KEY AUTOINCREMENT,
tipo_sanguineo TEXT NOT NULL,
fator_rh TEXT NOT NULL,
elegivel TEXT NOT NULL,
altura REAL NOT NULL,
peso REAL NOT NULL,
profissao TEXT NOT NULL,
contato_emergencia TEXT NOT NULL,
telefone_emergencia TEXT NOT NULL,
FOREIGN KEY (cod_doador) REFERENCES usuario(cod_usuario)
)
"""

INSERIR = """
INSERT INTO doador (cod_doador, tipo_sanguineo, fator_rh, elegivel, altura, peso, profissao, contato_emergencia, telefone_emergencia) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

OBTER_TODOS = """
SELECT d.cod_doador, d.tipo_sanguineo, d.fator_rh, d.elegivel, d.altura, d.peso, d.profissao, d.contato_emergencia, d.telefone_emergencia
FROM doador d,
usuario o
WHERE d.cod_doador = o.cod_usuario
""" 

UPDATE = """
UPDATE doador
SET tipo_sanguineo = ?, fator_rh = ?, elegivel = ?, altura = ?, peso = ?, profissao = ?, contato_emergencia = ?, telefone_emergencia = ?
WHERE cod_doador = ?;
"""

DELETE = """
DELETE FROM doador
WHERE cod_doador = ?;
"""

OBTER_POR_ID = """
SELECT d.cod_doador, d.tipo_sanguineo, d.fator_rh, d.elegivel, d.altura, d.peso, d.profissao, d.contato_emergencia, d.telefone_emergencia
FROM doador d,
usuario o
WHERE d.cod_doador = o.cod_usuario
AND d.cod_doador = ?;
"""

# OBTER_IDADE = """
# SELECT data_nascimento 
# FROM doador d,
# usuario o,
# doacao e,
# agendamento a
# WHERE d.cod_doador = o.cod_usuario
# AND d.cod_doacao = e.cod_doacao
# AND d.cod_agendamento = a.cod_agendamento
# WHERE cod_doador = ?
# """