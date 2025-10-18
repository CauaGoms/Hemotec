#!/usr/bin/env python
import sys
sys.path.insert(0, 'c:\\Users\\lucas\\Documents\\Hemotec\\Hemotec')

from data.repo import agendamento_repo

# Testar obter_por_id(3)
agendamento = agendamento_repo.obter_por_id(3)

print(f"\n=== RESULTADO obter_por_id(3) ===")
print(f"Agendamento: {agendamento}")
if agendamento:
    print(f"  cod_agendamento: {agendamento.cod_agendamento}")
    print(f"  cod_doador: {agendamento.cod_doador}")
    print(f"  data_hora: {agendamento.data_hora} (tipo: {type(agendamento.data_hora)})")
    print(f"  status: {agendamento.status}")
    print(f"  tipo_agendamento: {agendamento.tipo_agendamento}")
    print(f"  local_agendamento: {agendamento.local_agendamento}")
    print(f"  cod_colaborador: {agendamento.cod_colaborador}")
    
    # Tentar formatar data se existir
    if agendamento.data_hora:
        try:
            formatted = agendamento.data_hora.strftime('%d/%m/%Y às %H:%M')
            print(f"  Data formatada: {formatted}")
        except Exception as e:
            print(f"  Erro ao formatar data: {e}")
else:
    print("Agendamento é None!")
