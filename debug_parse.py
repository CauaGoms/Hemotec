from datetime import datetime

data_str = '2025-10-21 09:00:00'

try:
    data_hora = datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')
    print(f"Parse sucesso: {data_hora}")
    print(f"Tipo: {type(data_hora)}")
    print(f"Formatado: {data_hora.strftime('%d/%m/%Y às %H:%M')}")
except ValueError as e:
    print(f"Erro no parse: {e}")
