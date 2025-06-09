CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS gestor (
cod_gestor INTEGER PRIMARY KEY,
cnpj TEXT NOT NULL,
instituicao TEXT NOT NULL,
FOREIGN KEY (cod_gestor) REFERENCES usuario(cod_usuario),
FOREIGN KEY (cnpj) REFERENCES instituicao(cnpj)
)
"""

INSERIR = """
INSERT INTO gestor (cod_gestor, cnpj, instituicao) 
VALUES (?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
cod_gestor, cnpj, instituicao
FROM gestor
""" 