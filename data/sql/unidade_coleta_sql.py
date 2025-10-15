CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS unidade_coleta (
cod_unidade INTEGER PRIMARY KEY AUTOINCREMENT,
cod_licenca INTEGER NOT NULL,
cod_horario_funcionamento INTEGER NOT NULL,  
nome TEXT NOT NULL,
email TEXT NOT NULL,
rua_unidade TEXT NOT NULL,
bairro_unidade TEXT NOT NULL,
cidade_unidade INTEGER NOT NULL,
cep_unidade TEXT NOT NULL,
latitude REAL NOT NULL,
longitude REAL NOT NULL,
telefone TEXT NOT NULL,
FOREIGN KEY (cod_licenca) REFERENCES licenca(cod_licenca),
FOREIGN KEY (cidade_unidade) REFERENCES cidade(cod_cidade),
FOREIGN KEY (cod_horario_funcionamento) REFERENCES horario_funcionamento(cod_horario_funcionamento)
)
"""

INSERIR = """
INSERT INTO unidade_coleta (cod_licenca, cod_horario_funcionamento, nome, email, rua_unidade, bairro_unidade, cidade_unidade, cep_unidade, latitude, longitude, telefone) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT u.cod_unidade, l.cod_licenca, u.cod_horario_funcionamento, u.nome, u.email, u.rua_unidade, u.bairro_unidade, u.cidade_unidade, u.cep_unidade, u.latitude, u.longitude, u.telefone
FROM unidade_coleta u,
licenca l,
cidade c,
horario_funcionamento h
WHERE u.cod_licenca = l.cod_licenca
AND u.cod_horario_funcionamento = h.cod_horario_funcionamento
AND u.cidade_unidade = c.cod_cidade
""" 

UPDATE = """
UPDATE unidade_coleta
SET cod_licenca = ?, cod_horario_funcionamento = ?, nome = ?, email = ?, rua_unidade = ?, bairro_unidade = ?, cidade_unidade = ?, cep_unidade = ?, latitude = ?, longitude = ?, telefone = ?
WHERE cod_unidade = ?;
"""

DELETE = """
DELETE FROM unidade_coleta
WHERE cod_unidade = ?;
"""

OBTER_POR_ID = """
SELECT u.cod_unidade, l.cod_licenca, u.cod_horario_funcionamento, u.nome, u.email, u.rua_unidade, u.bairro_unidade, u.cidade_unidade, u.cep_unidade, u.latitude, u.longitude, u.telefone
FROM unidade_coleta u,
licenca l,
cidade c,
horario_funcionamento h
WHERE u.cod_licenca = l.cod_licenca
AND u.cidade_unidade = c.cod_cidade
AND u.cod_horario_funcionamento = h.cod_horario_funcionamento
AND u.cod_unidade = ?;
"""