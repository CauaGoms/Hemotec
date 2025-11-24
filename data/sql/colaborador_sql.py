CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS colaborador (
cod_colaborador INTEGER PRIMARY KEY AUTOINCREMENT,
cod_unidade INTEGER NOT NULL,
funcao TEXT NOT NULL,
FOREIGN KEY (cod_colaborador) REFERENCES usuario(cod_usuario),
FOREIGN KEY (cod_unidade) REFERENCES unidade_coleta(cod_unidade)
)
"""

INSERIR = """
INSERT INTO colaborador (cod_colaborador, cod_unidade, funcao) 
VALUES (?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
    c.cod_colaborador, 
    c.funcao,
    c.cod_unidade,
    u.cod_usuario,
    u.nome,
    u.email,
    u.senha,
    u.cpf,
    u.data_nascimento,
    u.status,
    u.data_cadastro,
    u.rua_usuario,
    u.bairro_usuario,
    u.cidade_usuario,
    u.cep_usuario,
    u.telefone,
    u.genero,
    u.perfil,
    u.foto,
    u.token_redefinicao,
    u.data_token,
    u.estado_usuario
FROM colaborador c
JOIN usuario u ON c.cod_colaborador = u.cod_usuario
"""

UPDATE = """
UPDATE colaborador
SET funcao = ?, cod_unidade = ?
WHERE cod_colaborador = ?;
"""

DELETE = """
DELETE FROM colaborador
WHERE cod_colaborador = ?;
"""

OBTER_POR_ID = """
SELECT 
    c.cod_colaborador, 
    c.funcao,
    c.cod_unidade,
    u.cod_usuario,
    u.nome,
    u.email,
    u.senha,
    u.cpf,
    u.data_nascimento,
    u.status,
    u.data_cadastro,
    u.rua_usuario,
    u.bairro_usuario,
    u.cidade_usuario,
    u.cep_usuario,
    u.telefone,
    u.genero,
    u.perfil,
    u.foto,
    u.token_redefinicao,
    u.data_token,
    u.estado_usuario
FROM colaborador c
JOIN usuario u ON c.cod_colaborador = u.cod_usuario
WHERE c.cod_colaborador = ?;
"""