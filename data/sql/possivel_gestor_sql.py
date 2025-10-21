CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS possivel_gestor (
cod_possivel_gestor INTEGER PRIMARY KEY AUTOINCREMENT,
nome_possivel_gestor TEXT NOT NULL,
email_possivel_gestor TEXT NOT NULL,
telefone_possivel_gestor TEXT NOT NULL,
cargo_possivel_gestor TEXT NOT NULL
)
"""

INSERIR = """
INSERT INTO possivel_gestor (nome_possivel_gestor, email_possivel_gestor, telefone_possivel_gestor, cargo_possivel_gestor) 
VALUES (?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT pg.cod_possivel_gestor, pg.nome_possivel_gestor, pg.email_possivel_gestor, pg.telefone_possivel_gestor, pg.cargo_possivel_gestor
FROM possivel_gestor pg
""" 

UPDATE = """
UPDATE possivel_gestor
SET nome_possivel_gestor = ?, email_possivel_gestor = ?, telefone_possivel_gestor = ?, cargo_possivel_gestor = ?
WHERE cod_possivel_gestor = ?;
"""

DELETE = """
DELETE FROM possivel_gestor
WHERE cod_possivel_gestor = ?;
"""

OBTER_POR_ID = """
SELECT pg.cod_possivel_gestor, pg.nome_possivel_gestor, pg.email_possivel_gestor, pg.telefone_possivel_gestor, pg.cargo_possivel_gestor
FROM possivel_gestor pg
WHERE pg.cod_possivel_gestor = ?;
"""

OBTER_POR_EMAIL = """
SELECT pg.cod_possivel_gestor, pg.nome_possivel_gestor, pg.email_possivel_gestor, pg.telefone_possivel_gestor, pg.cargo_possivel_gestor
FROM possivel_gestor pg
WHERE pg.email_possivel_gestor = ?;
"""

VERIFICAR_EMAIL_EXISTE = """
SELECT COUNT(*) as count
FROM possivel_gestor
WHERE email_possivel_gestor = ?;
"""

OBTER_POR_CARGO = """
SELECT pg.cod_possivel_gestor, pg.nome_possivel_gestor, pg.email_possivel_gestor, pg.telefone_possivel_gestor, pg.cargo_possivel_gestor
FROM possivel_gestor pg
WHERE pg.cargo_possivel_gestor = ?
ORDER BY pg.nome_possivel_gestor;
"""
