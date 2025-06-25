CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS assinatura (
cod_assinatura INTEGER PRIMARY KEY AUTOINCREMENT,
cnpj TEXT NOT NULL,
cod_plano INTEGER NOT NULL,
cod_licenca INTEGER NOT NULL,
data_inicio TEXT NOT NULL,
data_fim TEXT NOT NULL,
valor REAL NOT NULL,
qtd_licenca INTEGER NOT NULL,
FOREIGN KEY (cnpj) REFERENCES instituicao(cnpj),
FOREIGN KEY (cod_plano) REFERENCES plano(cod_plano),
FOREIGN KEY (cod_licenca) REFERENCES licenca(cod_licenca)
)
"""

INSERIR = """
INSERT INTO assinatura (cnpj, cod_plano, cod_licenca, data_inicio, data_fim, valor, qtd_licenca) 
VALUES (?, ?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT a.cod_assinatura, i.cnpj, p.cod_plano, l.cod_licenca, a.data_inicio, a.data_fim, a.valor, a.qtd_licenca
FROM assinatura a,
instituicao i,
plano p,
licenca l
WHERE a.cnpj = i.cnpj
AND a.cod_plano = p.cod_plano
AND a.cod_licenca = l.cod_licenca
""" 

UPDATE = """
UPDATE assinatura
SET cnpj = ?, cod_plano = ?, cod_licenca = ?, data_inicio = ?, data_fim = ?, valor = ?, qtd_licenca = ?
WHERE cod_assinatura = ?;
"""

DELETE = """
DELETE FROM assinatura
WHERE cod_assinatura = ?;
"""

OBTER_POR_ID = """
SELECT a.cod_assinatura, i.cnpj, p.cod_plano, l.cod_licenca, a.data_inicio, a.data_fim, a.valor, a.qtd_licenca
FROM assinatura a,
instituicao i,
plano p,
licenca l
WHERE a.cnpj = i.cnpj
AND a.cod_plano = p.cod_plano
AND a.cod_licenca = l.cod_licenca
AND a.cod_assinatura = ?;
"""