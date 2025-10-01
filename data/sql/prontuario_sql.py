CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS prontuario (
cod_prontuario INTEGER PRIMARY KEY AUTOINCREMENT,
cod_doacao INTEGER NOT NULL, 
data_criacao INTEGER NOT NULL,
data_atualizacao INTEGER NOT NULL,
diabetes INTEGER NOT NULL,
hipertensao INTEGER NOT NULL,
cardiopatia INTEGER NOT NULL,
cancer INTEGER NOT NULL,
nenhuma INTEGER NOT NULL,
outros INTEGER NOT NULL,
medicamentos TEXT NOT NULL,
fumante TEXT NOT NULL,
alcool TEXT NOT NULL,
atividade TEXT NOT NULL,
jejum TEXT NOT NULL,
sono TEXT NOT NULL,
bebida TEXT NOT NULL,
sintomas_gripais TEXT NOT NULL,
tatuagem TEXT NOT NULL,
termos TEXT NOT NULL,
alerta TEXT NOT NULL,
FOREIGN KEY (cod_doacao) REFERENCES doacao(cod_doacao)
)
"""

INSERIR = """
INSERT INTO prontuario (
cod_doacao, data_criacao, data_atualizacao, diabetes, hipertensao, cardiopatia, cancer, nenhuma, outros, medicamentos, fumante, alcool, atividade, jejum, sono, bebida, sintomas_gripais, tatuagem, termos, alerta
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

OBTER_TODOS = """
SELECT p.cod_prontuario, d.cod_doacao, p.data_criacao, p.data_atualizacao,
p.diabetes, p.hipertensao, p.cardiopatia, p.cancer, p.nenhuma, p.outros, p.medicamentos, p.fumante, p.alcool, p.atividade, p.jejum, p.sono, p.bebida, p.sintomas_gripais, p.tatuagem, p.termos, p.alerta
FROM prontuario p, 
doacao d
WHERE p.cod_doacao = d.cod_doacao
""" 

UPDATE = """
UPDATE prontuario
SET cod_doacao = ?, data_criacao = ?, data_atualizacao = ?, diabetes = ?, hipertensao = ?,
cardiopatia = ?, cancer = ?, nenhuma = ?, outros = ?, medicamentos = ?, fumante = ?, alcool = ?, atividade = ?, jejum = ?, sono = ?, bebida = ?, sintomas_gripais = ?, tatuagem = ?, termos = ?, alerta = ?
WHERE cod_prontuario = ?;
"""

DELETE = """
DELETE FROM prontuario
WHERE cod_prontuario = ?;
"""

OBTER_POR_ID = """
SELECT p.cod_prontuario, d.cod_doacao, p.data_criacao, p.data_atualizacao, p.diabetes, p.hipertensao, p.cardiopatia, p.cancer, p.nenhuma, p.outros, p.medicamentos, p.fumante, p.alcool, p.atividade, p.jejum, p.sono, p.bebida, p.sintomas_gripais, p.tatuagem, p.termos, p.alerta
FROM prontuario p, 
doacao d
WHERE p.cod_doacao = d.cod_doacao
AND p.cod_prontuario = ?;
"""