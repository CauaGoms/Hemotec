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