import sqlite3

conn = sqlite3.connect("dados.db")
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Query para agendamento 3
c.execute("SELECT * FROM agendamento WHERE cod_agendamento = 3")
row = c.fetchone()
if row:
    print(f"Agendamento 3: {dict(row)}")
    print(f"data_hora: '{row['data_hora']}' (tipo: {type(row['data_hora'])})")
else:
    print("Agendamento 3 não encontrado")

# Query JOIN como no repositório
c.execute("""
SELECT a.cod_agendamento, a.cod_colaborador, d.cod_doador, a.data_hora, a.status, a.tipo_agendamento, a.local_agendamento
FROM agendamento a
INNER JOIN doador d ON a.cod_doador = d.cod_doador
INNER JOIN unidade_coleta u ON a.local_agendamento = u.cod_unidade
LEFT JOIN colaborador c ON a.cod_colaborador = c.cod_colaborador
WHERE a.cod_agendamento = 3
""")
row = c.fetchone()
if row:
    print(f"\nAgendamento 3 (com JOIN): {dict(row)}")
    print(f"data_hora: '{row['data_hora']}' (tipo: {type(row['data_hora'])})")
else:
    print("Agendamento 3 não encontrado com JOIN")

conn.close()
