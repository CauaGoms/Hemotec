CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS adm_campanha (
cod_adm INTEGER NOT NULL,
cod_campanha INTEGER NOT NULL,
papel TEXT NOT NULL,
PRIMARY KEY (cod_adm, cod_campanha),
FOREIGN KEY (cod_adm) REFERENCES adm_unidade(cod_adm),
FOREIGN KEY (cod_campanha) REFERENCES campanha(cod_campanha)
)
"""

INSERIR = """
INSERT INTO adm_campanha (cod_adm, cod_campanha, papel) 
VALUES (?, ?, ?)
"""

OBTER_TODOS = """
SELECT adm.cod_adm, c.cod_campanha, adm.papel
FROM adm_campanha adm,
campanha c,
adm_unidade au
WHERE adm.cod_campanha = c.cod_campanha
AND adm.cod_adm = au.cod_adm
""" 

UPDATE = """
UPDATE adm_campanha
SET cod_campanha = ?, papel = ?
WHERE cod_adm = ?;
"""

DELETE = """
DELETE FROM adm_campanha
WHERE cod_adm = ?;
"""

OBTER_POR_ID = """
SELECT adm.cod_adm, c.cod_campanha, adm.papel
FROM adm_campanha adm,
campanha c,
adm_unidade au
WHERE adm.cod_adm = c.cod_campanha 
AND adm.cod_adm = au.cod_adm
AND adm.cod_adm = ?;
"""