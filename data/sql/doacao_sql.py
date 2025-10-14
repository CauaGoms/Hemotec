CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS doacao (
cod_doacao INTEGER PRIMARY KEY AUTOINCREMENT,
cod_doador INTEGER NOT NULL,
cod_agendamento INTEGER,
data_hora TEXT,
quantidade INTEGER,
status INTEGER,
observacoes TEXT,
FOREIGN KEY (cod_doador) REFERENCES doador(cod_doador),
FOREIGN KEY (cod_agendamento) REFERENCES agendamento(cod_agendamento)
)
"""

INSERIR = """
INSERT INTO doacao (cod_doador, cod_agendamento, data_hora, quantidade, status, observacoes) 
VALUES (?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT d.cod_doacao, o.cod_doador, d.cod_agendamento, d.data_hora, d.quantidade, d.status, d.observacoes
FROM doacao d,
doador o
WHERE d.cod_doador = o.cod_doador
""" 

UPDATE = """
UPDATE doacao
SET cod_doador = ?, cod_agendamento = ?, data_hora = ?, quantidade = ?, status = ?, observacoes = ?
WHERE cod_doacao = ?;
"""

DELETE = """
DELETE FROM doacao
WHERE cod_doacao = ?;
"""

OBTER_POR_ID = """
SELECT d.cod_doacao, o.cod_doador, d.cod_agendamento, d.data_hora, d.quantidade, d.status, d.observacoes
FROM doacao d,
doador o
WHERE d.cod_doador = o.cod_doador
AND d.cod_doacao = ?;
"""

OBTER_DOACOES_COMPLETAS_POR_DOADOR = """
SELECT 
    d.cod_doacao,
    d.cod_doador,
    d.cod_agendamento,
    d.data_hora,
    d.quantidade,
    d.status,
    d.observacoes,
    u.nome as nome_doador,
    do.tipo_sanguineo,
    do.fator_rh,
    uc.nome as nome_unidade,
    uc.rua_unidade,
    uc.bairro_unidade,
    uc.cep_unidade,
    uc.telefone as telefone_unidade,
    c.nome_cidade,
    c.sigla_estado,
    a.data_hora as data_hora_agendamento
FROM doacao d
INNER JOIN doador do ON d.cod_doador = do.cod_doador
INNER JOIN usuario u ON do.cod_doador = u.cod_usuario
LEFT JOIN agendamento a ON d.cod_agendamento = a.cod_agendamento
LEFT JOIN unidade_coleta uc ON a.local_agendamento = uc.cod_unidade
LEFT JOIN cidade c ON uc.cidade_unidade = c.cod_cidade
WHERE d.cod_doador = ?
ORDER BY d.data_hora DESC;
"""