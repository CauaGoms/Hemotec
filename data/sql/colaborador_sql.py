CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS colaborador (
cod_colaborador INTEGER PRIMARY KEY AUTOINCREMENT,
funcao TEXT NOT NULL,
FOREIGN KEY (cod_colaborador) REFERENCES usuario(cod_usuario)
)
"""

INSERIR = """
INSERT INTO colaborador (cod_colaborador, funcao) 
VALUES (?, ?)
"""

OBTER_TODOS = """
SELECT u.cod_colaborador, c.funcao
FROM colaborador c,
usuario u
WHERE c.cod_colaborador = u.cod_usuario
""" 

UPDATE = """
UPDATE colaborador
SET funcao = ?
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
    u.telefone
FROM colaborador c
JOIN usuario u ON c.cod_colaborador = u.cod_usuario
WHERE c.cod_colaborador = ?;
"""