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