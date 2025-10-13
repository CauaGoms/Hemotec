CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS doacao (
cod_doacao INTEGER PRIMARY KEY AUTOINCREMENT,
cod_doador INTEGER NOT NULL,
data_hora TEXT,
quantidade INTEGER,
status INTEGER,
FOREIGN KEY (cod_doador) REFERENCES doador(cod_doador)
)
"""

INSERIR = """
INSERT INTO doacao (cod_doador, data_hora, quantidade, status) 
VALUES (?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT d.cod_doacao, o.cod_doador, d.data_hora, d.quantidade, d.status
FROM doacao d,
doador o
WHERE d.cod_doador = o.cod_doador
""" 

UPDATE = """
UPDATE doacao
SET cod_doador = ?, data_hora = ?, quantidade = ?, status = ?
WHERE cod_doacao = ?;
"""

DELETE = """
DELETE FROM doacao
WHERE cod_doacao = ?;
"""

OBTER_POR_ID = """
SELECT d.cod_doacao, o.cod_doador, d.data_hora, d.quantidade, d.status
FROM doacao d,
doador o
WHERE d.cod_doador = o.cod_doador
AND d.cod_doacao = ?;
"""

OBTER_DOACOES_COMPLETAS_POR_DOADOR = """
SELECT 
    d.cod_doacao,
    d.cod_doador,
    d.data_hora,
    d.quantidade,
    d.status,
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
    a.observacoes
FROM doacao d
INNER JOIN doador do ON d.cod_doador = do.cod_doador
INNER JOIN usuario u ON do.cod_doador = u.cod_usuario
LEFT JOIN agendamento a ON a.cod_doador = d.cod_doador 
    AND datetime(a.data_hora) <= datetime(d.data_hora)
LEFT JOIN unidade_coleta uc ON a.local_agendamento = uc.cod_unidade
LEFT JOIN cidade c ON uc.cidade_unidade = c.cod_cidade
WHERE d.cod_doador = ?
ORDER BY d.data_hora DESC;
"""