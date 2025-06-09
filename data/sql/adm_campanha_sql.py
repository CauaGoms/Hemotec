CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS adm_campanha (
cod_adm INTEGER PRIMARY KEY NOT NULL,
cod_campanha INTEGER PRIMARY KEY NOT NULL,
papel TEXT NOT NULL,
FOREIGN KEY (cod_adm) REFERENCES adm(cod_adm),
FOREIGN KEY (cod_campanha) REFERENCES campanha(cod_campanha)
)
"""

INSERIR = """
INSERT INTO adm_campanha (cod_adm, cod_campanha, papel) 
VALUES (?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
cod_adm, cod_campanha, papel
FROM adm_campanha
""" 

UPDATE = """
UPDATE adm_campanha
SET papel = ?
WHERE cod_adm = ? AND cod_campanha = ?
"""

DELETE = """
DELETE FROM adm_campanha
WHERE cod_adm = ? AND cod_campanha = ?
"""

OBTER_POR_ID = """
SELECT adm.cod_adm, adm.cod_campanha, adm.papel
cod_adm, cod_campanha, papel
FROM adm_campanha adm
WHERE cod_adm = ? AND cod_campanha = ?
"""