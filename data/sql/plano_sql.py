CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS plano (
cod_plano INTEGER PRIMARY KEY AUTOINCREMENT,
cod_assinatura INTEGER NOT NULL, 
qtd_licenca INTEGER NOT NULL,
nome TEXT NOT NULL,
valor REAL NOT NULL,
validade INTEGER NOT NULL,
FOREIGN KEY (cod_assinatura) REFERENCES assinatura(cod_assinatura)
)
"""

INSERIR = """
INSERT INTO plano (cod_assinatura, qtd_licenca, nome, valor, validade) 
VALUES (?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT p.cod_plano, a.cod_assinatura, p.qtd_licenca, p.nome, p.valor, p.validade
FROM plano p, 
assinatura a
WHERE p.cod_assinatura = a.cod_assinatura
""" 

UPDATE = """
UPDATE plano
SET cod_assinatura = ?, qtd_licenca = ?, nome = ?, valor = ?, validade = ?
WHERE cod_plano = ?;
"""

DELETE = """
DELETE FROM plano
WHERE cod_plano = ?;
"""

OBTER_POR_ID = """
SELECT p.cod_plano, a.cod_assinatura, p.qtd_licenca, p.nome, p.valor, p.validade
FROM plano p, 
assinatura a
WHERE p.cod_assinatura = a.cod_assinatura
AND p.cod_plano = ?;
"""