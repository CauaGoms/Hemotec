CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS prontuario (
cod_prontuario INTEGER PRIMARY KEY AUTOINCREMENT,
cod_doador INTEGER NOT NULL, 
data_criacao INTEGER NOT NULL,
data_atualizacao INTEGER NOT NULL,
diabetes INTEGER NOT NULL,
hipertensao INTEGER NOT NULL,
cardiopatia INTEGER NOT NULL,
epilepsia INTEGER NOT NULL,
cancer INTEGER NOT NULL,
nenhuma INTEGER NOT NULL,
outros INTEGER NOT NULL,
outros_detalhe TEXT,
medicamentos TEXT NOT NULL,
fumante TEXT NOT NULL,
alcool TEXT NOT NULL,
atividade TEXT NOT NULL,
FOREIGN KEY (cod_doador) REFERENCES doador(cod_doador)
)
"""

INSERIR = """
INSERT INTO prontuario (
cod_doador, data_criacao, data_atualizacao, diabetes, hipertensao,
cardiopatia, epilepsia, cancer, nenhuma, outros, outros_detalhe,
medicamentos, fumante, alcool, atividade
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

OBTER_TODOS = """
SELECT p.cod_prontuario, d.cod_doador, p.data_criacao, p.data_atualizacao,
p.diabetes, p.hipertensao, p.cardiopatia, p.epilepsia, p.cancer,
p.nenhuma, p.outros, p.outros_detalhe, p.medicamentos,
p.fumante, p.alcool, p.atividade
FROM prontuario p, 
doador d
WHERE p.cod_doador = d.cod_doador
""" 

UPDATE = """
UPDATE prontuario
SET cod_assinatura = ?, qtd_licenca = ?, nome = ?, valor = ?, validade = ?
WHERE cod_plano = ?;
"""

DELETE = """
DELETE FROM plano
WHERE cod_plano = ?;
"""

OBTER_POR_ID = """
SELECT p.cod_plano, a.cod_assinatura, p.qtd_licenca, p.nome, p.valor, p.validade
FROM plano p, 
assinatura a
WHERE p.cod_assinatura = a.cod_assinatura
AND p.cod_plano = ?;
"""