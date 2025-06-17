CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS instituicao (
cnpj INTEGER PRIMARY KEY NOT NULL,
cod_gestor INTEGER NOT NULL,
cod_assinatura INTEGER NOT NULL, 
nome TEXT NOT NULL,
email TEXT NOT NULL, 
rua_instituicao TEXT NOT NULL, 
bairro_instituicao TEXT NOT NULL,
cidade_instituicao INTEGER NOT NULL,
cep_instituicao TEXT NOT NULL,
FOREIGN KEY (cod_gestor) REFERENCES gestor(cod_gestor),
FOREIGN KEY (cod_assinatura) REFERENCES assinatura(cod_assinatura),
FOREIGN KEY (cidade_instituicao) REFERENCES cidade(cod_cidade)
)
"""

INSERIR = """
INSERT INTO instituicao (cnpj, cod_gestor, cod_assinatura, nome, email, rua_instituicao, bairro_instituicao, cidade_instituicao, cep_instituicao) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
cnpj, cod_gestor, cod_assinatura, nome, email, rua_instituicao, bairro_instituicao, cidade_instituicao, cep_instituicao
FROM instituicao
"""

UPDATE = """
UPDATE cnpj, cod_gestor, cod_assinatura, nome, email, rua_instituicao, bairro_instituicao, cidade_instituicao, cep_instituicao
SET cod_gestor = ?, cod_assinatura = ?, nome = ?, email = ?, rua_instituicao = ?, bairro_instituicao = ?, cidade_instituicao = ?, cep_instituicao = ?
WHERE cnpj = ?;
"""

DELETE = """
DELETE FROM instituicao
WHERE cnpj = ?;
"""

OBTER_POR_ID = """
SELECT i.cnpj, g.cod_gestor, a.cod_assinatura, i.nome, i.email, i.rua_instituicao, i.bairro_instituicao, c.cidade_instituicao, i.cep_instituicao
FROM instituicao i,
gestor g,
assinatura a,
cidade c
WHERE i.cod_gestor = g.cod_gestor
AND i.cod_assinatura = a.cod_assinatura
AND i.cidade_instituicao = c.cod_cidade
AND i.cnpj = ?;
"""