CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS instituicao (
cnpj INTEGER PRIMARY KEY ,
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