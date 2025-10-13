CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS prontuario (
cod_prontuario INTEGER PRIMARY KEY AUTOINCREMENT,
cod_doacao INTEGER NOT NULL, 
data_criacao INTEGER NOT NULL,
data_atualizacao INTEGER NOT NULL,
jejum INTEGER NOT NULL,
diabetes INTEGER NOT NULL,
hipertensao INTEGER NOT NULL,
cardiopatia INTEGER NOT NULL,
cancer INTEGER NOT NULL,
hepatite INTEGER NOT NULL,
outros INTEGER NOT NULL,
detalhes_outros TEXT NULL,
sintomas_gripais INTEGER NOT NULL,
medicamentos TEXT NOT NULL,
detalhes_medicamentos TEXT NULL,
fumante TEXT NOT NULL,
alcool TEXT NOT NULL,
droga TEXT NOT NULL,
ist TEXT NOT NULL,
atividade TEXT NOT NULL,
sono TEXT NOT NULL,
tatuagem_e_outros TEXT NOT NULL,
FOREIGN KEY (cod_doacao) REFERENCES doacao(cod_doacao)
)
"""

INSERIR = """
INSERT INTO prontuario (
cod_doacao, data_criacao, data_atualizacao, jejum, diabetes, hipertensao, cardiopatia, cancer, hepatite, outros, detalhes_outros, sintomas_gripais, medicamentos, detalhes_medicamentos, fumante, alcool, droga, ist, atividade, sono, tatuagem_e_outros
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

OBTER_TODOS = """
SELECT p.cod_prontuario, d.cod_doacao, p.data_criacao, p.data_atualizacao,
p.jejum, p.diabetes, p.hipertensao, p.cardiopatia, p.cancer, p.hepatite, p.outros, p.detalhes_outros, p.sintomas_gripais, p.medicamentos, p.detalhes_medicamentos, p.fumante, p.alcool, p.droga, p.ist, p.atividade, p.sono, p.tatuagem_e_outros
FROM prontuario p, 
doacao d
WHERE p.cod_doacao = d.cod_doacao
""" 

UPDATE = """
UPDATE prontuario
SET cod_doacao = ?, data_criacao = ?, data_atualizacao = ?, jejum = ?, diabetes = ?, hipertensao = ?, cardiopatia = ?, cancer = ?, hepatite = ?, outros = ?, detalhes_outros = ?, sintomas_gripais = ?, medicamentos = ?, detalhes_medicamentos = ?, fumante = ?, alcool = ?, droga = ?, ist = ?, atividade = ?, sono = ?, tatuagem_e_outros = ?
WHERE cod_prontuario = ?;
"""

DELETE = """
DELETE FROM prontuario
WHERE cod_prontuario = ?;
"""

OBTER_POR_ID = """
SELECT p.cod_prontuario, d.cod_doacao, p.data_criacao, p.data_atualizacao, p.jejum, p.diabetes, p.hipertensao, p.cardiopatia, p.cancer, p.hepatite, p.outros, p.detalhes_outros, p.sintomas_gripais, p.medicamentos, p.detalhes_medicamentos, p.fumante, p.alcool, p.droga, p.ist, p.atividade, p.sono, p.tatuagem_e_outros
FROM prontuario p, 
doacao d
WHERE p.cod_doacao = d.cod_doacao
AND p.cod_prontuario = ?;
"""

OBTER_POR_DOACAO = """
SELECT p.cod_prontuario, d.cod_doacao, p.data_criacao, p.data_atualizacao, p.jejum, p.diabetes, p.hipertensao, p.cardiopatia, p.cancer, p.hepatite, p.outros, p.detalhes_outros, p.sintomas_gripais, p.medicamentos, p.detalhes_medicamentos, p.fumante, p.alcool, p.droga, p.ist, p.atividade, p.sono, p.tatuagem_e_outros
FROM prontuario p, 
doacao d
WHERE p.cod_doacao = d.cod_doacao
AND p.cod_doacao = ?;
"""