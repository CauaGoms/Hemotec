CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS gestor (
cod_gestor INTEGER PRIMARY KEY,
cod_instituicao INTEGER NOT NULL,
instituicao TEXT NOT NULL,
FOREIGN KEY (cod_gestor) REFERENCES usuario(cod_usuario),
FOREIGN KEY (cod_instituicao) REFERENCES instituicao(cod_instituicao)
)
"""

INSERIR = """
INSERT INTO gestor (cod_gestor, cod_instituicao, instituicao) 
VALUES (?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
    g.cod_gestor, 
    g.cod_instituicao, 
    g.instituicao,
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
FROM gestor g
JOIN usuario u ON g.cod_gestor = u.cod_usuario
""" 

UPDATE = """
UPDATE gestor
SET cod_instituicao = ?, instituicao = ?
WHERE cod_gestor = ?;
"""

DELETE = """
DELETE FROM gestor
WHERE cod_gestor = ?;
"""

OBTER_POR_ID = """
SELECT 
    g.cod_gestor, 
    g.cod_instituicao,
    g.instituicao,
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
FROM gestor g
JOIN usuario u ON g.cod_gestor = u.cod_usuario
WHERE g.cod_gestor = ?;
"""