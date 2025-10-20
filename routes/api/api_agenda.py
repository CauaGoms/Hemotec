from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, date
from data.repo import agenda_repo

router = APIRouter()

@router.get("/api/agenda/horarios-disponiveis")
async def get_horarios_disponiveis(cod_unidade: int, data: str):
    """
    Retorna os horários disponíveis para uma unidade em uma data específica
    
    Parâmetros:
    - cod_unidade: ID da unidade de coleta
    - data: Data no formato YYYY-MM-DD
    
    Retorna:
    - Lista de horários com vagas disponíveis
    """
    try:
        # Converter string de data para objeto date
        data_agenda = datetime.strptime(data, '%Y-%m-%d').date()
        
        # Buscar agendas para a unidade e data
        agendas = agenda_repo.obter_por_unidade_e_data(cod_unidade, data_agenda)
        
        # Obter data e hora atual
        agora = datetime.now()
        data_hoje = agora.date()
        hora_atual = agora.time()
        
        # Filtrar apenas agendas com vagas disponíveis
        horarios_disponiveis = []
        for agenda in agendas:
            vagas_disponiveis = agenda.vagas - agenda.quantidade_doadores
            
            # Se tem vagas disponíveis
            if vagas_disponiveis > 0:
                # Se a data é hoje, verificar se o horário já passou
                if data_agenda == data_hoje:
                    # Só adicionar se o horário ainda não passou
                    if agenda.hora_agenda > hora_atual:
                        horarios_disponiveis.append({
                            "cod_agenda": agenda.cod_agenda,
                            "hora": agenda.hora_agenda.strftime('%H:%M'),
                            "vagas": agenda.vagas,
                            "ocupadas": agenda.quantidade_doadores,
                            "disponiveis": vagas_disponiveis
                        })
                else:
                    # Data futura, adicionar normalmente
                    horarios_disponiveis.append({
                        "cod_agenda": agenda.cod_agenda,
                        "hora": agenda.hora_agenda.strftime('%H:%M'),
                        "vagas": agenda.vagas,
                        "ocupadas": agenda.quantidade_doadores,
                        "disponiveis": vagas_disponiveis
                    })
        
        # Ordenar por horário
        horarios_disponiveis.sort(key=lambda x: x['hora'])
        
        return JSONResponse(content={
            "success": True,
            "data": horarios_disponiveis
        })
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Formato de data inválido. Use YYYY-MM-DD. Erro: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar horários: {str(e)}")


@router.get("/api/agenda/datas-disponiveis")
async def get_datas_disponiveis(cod_unidade: int, mes: int, ano: int):
    """
    Retorna as datas que têm horários disponíveis para uma unidade em um mês específico
    
    Parâmetros:
    - cod_unidade: ID da unidade de coleta
    - mes: Mês (1-12)
    - ano: Ano (ex: 2025)
    
    Retorna:
    - Lista de datas (dias do mês) que têm horários disponíveis
    """
    try:
        # Buscar todas as agendas da unidade
        agendas = agenda_repo.obter_por_unidade(cod_unidade)
        
        # Obter data e hora atual
        agora = datetime.now()
        data_hoje = agora.date()
        hora_atual = agora.time()
        
        # Agrupar agendas por data
        agendas_por_data = {}
        for agenda in agendas:
            if agenda.data_agenda.month == mes and agenda.data_agenda.year == ano:
                if agenda.data_agenda not in agendas_por_data:
                    agendas_por_data[agenda.data_agenda] = []
                agendas_por_data[agenda.data_agenda].append(agenda)
        
        # Filtrar datas com horários disponíveis
        datas_disponiveis = set()
        for data, agendas_dia in agendas_por_data.items():
            tem_horario_disponivel = False
            
            for agenda in agendas_dia:
                vagas_disponiveis = agenda.vagas - agenda.quantidade_doadores
                
                if vagas_disponiveis > 0:
                    # Se é hoje, verificar se o horário ainda não passou
                    if data == data_hoje:
                        if agenda.hora_agenda > hora_atual:
                            tem_horario_disponivel = True
                            break
                    else:
                        # Data futura
                        tem_horario_disponivel = True
                        break
            
            if tem_horario_disponivel:
                datas_disponiveis.add(data.day)
        
        return JSONResponse(content={
            "success": True,
            "datas": sorted(list(datas_disponiveis))
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar datas: {str(e)}")
