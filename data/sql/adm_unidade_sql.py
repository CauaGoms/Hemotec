CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS adm_unidade (
cod_adm INTEGER PRIMARY KEY NOT NULL,
cod_unidade INTEGER NOT NULL,
FOREIGN KEY (cod_adm) REFERENCES usuario(cod_usuario),
FOREIGN KEY (cod_unidade) REFERENCES unidade_coleta(cod_unidade)
)
"""

INSERIR = """
INSERT INTO adm_unidade (cod_adm, cod_unidade) 
VALUES (?, ?)
"""

OBTER_TODOS = """
SELECT usu.cod_usuario AS cod_adm, u.cod_unidade,
       usu.nome, usu.email, usu.senha, usu.cpf, usu.data_nascimento, usu.status, usu.data_cadastro,
       usu.rua_usuario, usu.bairro_usuario, usu.cidade_usuario, usu.cep_usuario, usu.telefone
FROM adm_unidade adm,
unidade_coleta u,
usuario usu
WHERE adm.cod_adm = usu.cod_usuario
AND adm.cod_unidade = u.cod_unidade
""" 

DELETE = """
DELETE FROM adm_unidade
WHERE cod_adm = ?;
"""

OBTER_POR_ID = """
SELECT adm.cod_adm,
    adm.cod_unidade,
    usu.nome,
    usu.email,
    usu.senha,
    usu.cpf,
    usu.data_nascimento,
    usu.status,
    usu.data_cadastro,
    usu.rua_usuario,
    usu.bairro_usuario,
    usu.cidade_usuario,
    usu.cep_usuario,
    usu.telefone
FROM adm_unidade adm,
unidade_coleta u,
usuario usu
WHERE adm.cod_adm = usu.cod_usuario
AND adm.cod_unidade = u.cod_unidade
AND adm.cod_adm = ?;
"""