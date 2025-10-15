CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS horario_funcionamento (
cod_horario_funcionamento INTEGER PRIMARY KEY AUTOINCREMENT,
horario_inicio TIME NOT NULL,
horario_fim TIME NOT NULL,
intervalo_doacoes INTEGER NOT NULL,
data DATE NOT NULL
)
"""

INSERIR = """
INSERT INTO horario_funcionamento (horario_inicio, horario_fim, intervalo_doacoes, data) 
VALUES (?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT h.cod_horario_funcionamento, h.horario_inicio, h.horario_fim, h.intervalo_doacoes, h.data
FROM horario_funcionamento h
""" 

UPDATE = """
UPDATE horario_funcionamento
SET horario_inicio = ?, horario_fim = ?, intervalo_doacoes = ?, data = ?
WHERE cod_horario_funcionamento = ?;
"""

DELETE = """
DELETE FROM horario_funcionamento
WHERE cod_horario_funcionamento = ?;
"""

OBTER_POR_ID = """
SELECT h.cod_horario_funcionamento, h.horario_inicio, h.horario_fim, h.intervalo_doacoes, h.data
FROM horario_funcionamento h
WHERE h.cod_horario_funcionamento = ?;
"""

OBTER_POR_DATA = """
SELECT h.cod_horario_funcionamento, h.horario_inicio, h.horario_fim, h.intervalo_doacoes, h.data
FROM horario_funcionamento h
WHERE h.data = ?
ORDER BY h.horario_inicio;
"""

OBTER_POR_PERIODO = """
SELECT h.cod_horario_funcionamento, h.horario_inicio, h.horario_fim, h.intervalo_doacoes, h.data
FROM horario_funcionamento h
WHERE h.data BETWEEN ? AND ?
ORDER BY h.data, h.horario_inicio;
"""

VERIFICAR_DISPONIBILIDADE = """
SELECT h.cod_horario_funcionamento, h.horario_inicio, h.horario_fim, h.intervalo_doacoes, h.data
FROM horario_funcionamento h
WHERE h.data = ? 
  AND h.horario_inicio <= ? 
  AND h.horario_fim >= ?;
"""
