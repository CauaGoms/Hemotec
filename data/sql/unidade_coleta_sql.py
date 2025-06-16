CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS unidade_coleta (
cod_unidade INTEGER PRIMARY KEY AUTOINCREMENT,
cod_adm INTEGER NOT NULL,
cod_licenca INTEGER NOT NULL, 
cod_estoque INTEGER NOT NULL,  
nome TEXT NOT NULL,
email TEXT NOT NULL,
rua_unidade TEXT NOT NULL,
bairro_unidade TEXT NOT NULL,
cidade_unidade INTEGER NOT NULL,
cep_unidade TEXT NOT NULL,
FOREIGN KEY (cod_adm) REFERENCES adm_unidade(cod_adm),
FOREIGN KEY (cod_licenca) REFERENCES licenca(cod_licenca),
FOREIGN KEY (cod_estoque) REFERENCES estoque(cod_estoque),
FOREIGN KEY (cidade_unidade) REFERENCES cidade(cod_cidade)
)
"""

INSERIR = """
INSERT INTO unidade_coleta (cod_adm, cod_licenca, cod_estoque, nome, email, rua_unidade, bairro_unidade, cidade_unidade, cep_unidade) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
cod_unidade, cod_adm, cod_licenca, cod_estoque, nome, email, rua_unidade, bairro_unidade, cidade_unidade, cep_unidade
FROM unidade_coleta
""" 

UPDATE = """
UPDATE cod_unidade, cod_adm, cod_licenca, cod_estoque, nome, email, rua_unidade, bairro_unidade, cidade_unidade, cep_unidade
SET cod_adm = ?, cod_licenca = ?, cod_estoque = ?, nome = ?, email = ?, rua_unidade = ?, bairro_unidade = ?, cidade_unidade = ?, cep_unidade = ?
WHERE cod_unidade = ?;
"""

DELETE = """
DELETE FROM unidade_coleta
WHERE cod_unidade = ?;
"""

OBTER_POR_ID = """
SELECT u.cod_unidade, a.cod_adm, l.cod_licenca, e.cod_estoque, u.nome, u.email, u.rua_unidade, u.bairro_unidade, c.cod_cidade, u.cep_unidade
FROM unidade_coleta u,
adm_unidade a,
licenca l,
estoque e,
cidade c
WHERE u.cod_adm = a.cod_adm
AND u.cod_licenca = l.cod_licenca
AND u.cod_estoque = e.cod_estoque
AND u.cidade_unidade = c.cod_cidade
AND u.cod_unidade = ?;
"""