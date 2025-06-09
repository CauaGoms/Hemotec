CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS colaborador (
cod_colaborador INTEGER PRIMARY KEY AUTOINCREMENT,
cod_agendamento INTEGER NOT NULL,
funcao TEXT NOT NULL,
FOREIGN KEY (cod_colaborador) REFERENCES usuario(cod_usuario),
FOREIGN KEY (cod_agendamento) REFERENCES agendamento(cod_agendamento)
)
"""

INSERIR = """
INSERT INTO colaborador (cod_colaborador, cod_agendamento, funcao) 
VALUES (?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
cod_colaborador, cod_agendamento, funcao
FROM colaborador
""" 