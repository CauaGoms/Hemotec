from fastapi import APIRouter, HTTPException
from datetime import date, datetime
from data.repo import agenda_repo, agendamento_repo
from data.model.agendamento_model import Agendamento
from typing import List, Dict
from pydantic import BaseModel

router = APIRouter()

class CriarAgendamentoRequest(BaseModel):
    cod_usuario: int  # Alterado de cod_doador para cod_usuario
    cod_agenda: int
    data: str  # formato YYYY-MM-DD
    horario: str  # formato HH:MM

@router.get("/api/doador/agendamento/horarios-disponiveis")
async def get_horarios_disponiveis(cod_unidade: int, data: str):
    """
    Retorna os horários disponíveis para uma unidade em uma data específica.
    Considera apenas agendas onde quantidade_doadores < vagas.
    Filtra horários que já passaram do horário atual.
    """
    try:
        # Converte string de data para objeto date
        data_agenda = datetime.strptime(data, '%Y-%m-%d').date()
        
        # Busca todas as agendas para aquela unidade e data
        agendas = agenda_repo.obter_por_unidade_e_data(cod_unidade, data_agenda)
        
        # Obtém data e hora atual
        agora = datetime.now()
        data_hoje = agora.date()
        hora_atual = agora.time()
        
        # Filtra apenas horários com vagas disponíveis
        horarios_disponiveis = []
        for agenda in agendas:
            vagas_disponiveis = agenda.vagas - agenda.quantidade_doadores
            
            # Verifica se o horário já passou (somente para hoje)
            horario_passou = False
            if data_agenda == data_hoje:
                # Se for hoje, verifica se o horário já passou
                if agenda.hora_agenda <= hora_atual:
                    horario_passou = True
            
            # Apenas adiciona se tiver vagas disponíveis E o horário não tiver passado
            if vagas_disponiveis > 0 and not horario_passou:
                horarios_disponiveis.append({
                    "cod_agenda": agenda.cod_agenda,
                    "horario": agenda.hora_agenda.strftime('%H:%M'),
                    "vagas_totais": agenda.vagas,
                    "vagas_ocupadas": agenda.quantidade_doadores,
                    "vagas_disponiveis": vagas_disponiveis
                })
        
        # Ordena por horário
        horarios_disponiveis.sort(key=lambda x: x["horario"])
        
        return {
            "success": True,
            "data": data,
            "cod_unidade": cod_unidade,
            "horarios": horarios_disponiveis
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Formato de data inválido. Use YYYY-MM-DD. Erro: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar horários: {str(e)}")


@router.get("/api/doador/agendamento/datas-disponiveis")
async def get_datas_disponiveis(cod_unidade: int, mes: int, ano: int):
    """
    Retorna as datas que têm pelo menos um horário disponível em um determinado mês/ano.
    """
    try:
        # Busca todas as agendas da unidade
        agendas = agenda_repo.obter_por_unidade(cod_unidade)
        
        # Filtra por mês/ano e verifica disponibilidade
        datas_disponiveis = set()
        for agenda in agendas:
            # Verifica se é do mês/ano solicitado
            if agenda.data_agenda.month == mes and agenda.data_agenda.year == ano:
                # Verifica se tem vagas disponíveis
                vagas_disponiveis = agenda.vagas - agenda.quantidade_doadores
                if vagas_disponiveis > 0:
                    datas_disponiveis.add(agenda.data_agenda.strftime('%Y-%m-%d'))
        
        return {
            "success": True,
            "mes": mes,
            "ano": ano,
            "cod_unidade": cod_unidade,
            "datas": sorted(list(datas_disponiveis))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar datas disponíveis: {str(e)}")


@router.get("/api/doador/agendamento/verificar-disponibilidade")
async def verificar_disponibilidade_usuario(cod_usuario: int, data: str):
    """
    Verifica se o usuário pode realizar um agendamento na data especificada.
    Retorna erros se:
    - Já existe um agendamento pendente
    - Não cumpriu o intervalo mínimo desde a última doação
    """
    try:
        import sys
        from data.repo import usuario_repo, doacao_repo
        
        # Verifica se já existe agendamento pendente
        agendamentos_pendentes = agendamento_repo.obter_por_usuario_status(cod_usuario, status=0)
        if agendamentos_pendentes:
            return {
                "success": False,
                "pode_agendar": False,
                "motivo": "Você já possui um agendamento pendente. Aguarde ou cancele antes de criar outro."
            }
        
        # Busca o usuário para verificar gênero
        usuario = usuario_repo.obter_por_id(cod_usuario)
        if not usuario:
            return {
                "success": False,
                "pode_agendar": False,
                "motivo": "Usuário não encontrado no sistema."
            }
        
        # Converte a data para datetime
        data_agendamento = datetime.strptime(data, '%Y-%m-%d')
        
        # Busca última doação
        doacoes = doacao_repo.obter_doacoes_completas_por_doador(cod_usuario)
        ultima_doacao = None
        if doacoes:
            doacoes_concluidas = [d for d in doacoes if d.get('status') == 1 and d.get('data_hora')]
            if doacoes_concluidas:
                ultima_doacao = doacoes_concluidas[0]['data_hora']
        
        # Valida intervalo mínimo entre doações
        if ultima_doacao:
            dias_entre = (data_agendamento.date() - ultima_doacao.date()).days
            genero = (usuario.genero or '').lower()
            if genero == 'masculino':
                intervalo_min = 60
            else:
                intervalo_min = 90
            
            if dias_entre < intervalo_min:
                return {
                    "success": False,
                    "pode_agendar": False,
                    "motivo": f"É necessário aguardar pelo menos {intervalo_min} dias entre doações. Última doação: {ultima_doacao.strftime('%d/%m/%Y')}."
                }
        
        # Tudo OK, pode agendar
        return {
            "success": True,
            "pode_agendar": True,
            "motivo": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "pode_agendar": False,
            "motivo": f"Erro ao verificar disponibilidade: {str(e)}"
        }


@router.post("/api/doador/agendamento/criar")
async def criar_agendamento(request: CriarAgendamentoRequest):
    """
    Cria um novo agendamento para o usuário.
    - Verifica se há vagas disponíveis
    - Incrementa quantidade_doadores na agenda
    - Insere o agendamento na tabela agendamentos
    - cod_colaborador = NULL (agendamento online)
    - tipo_agendamento = 'online'
    - status = 0 (não concluído)
    """
    try:
        # Debug: Log dos dados recebidos
        import sys
        from data.repo import usuario_repo, doacao_repo
        sys.stderr.write(f"DEBUG - Dados recebidos: cod_usuario={request.cod_usuario}, cod_agenda={request.cod_agenda}, data={request.data}, horario={request.horario}\n")
        sys.stderr.flush()
        # Verifica se já existe agendamento pendente para o usuário
        agendamentos_pendentes = agendamento_repo.obter_por_usuario_status(request.cod_usuario, status=0)
        if agendamentos_pendentes:
            raise HTTPException(status_code=400, detail="Você já possui um agendamento pendente. Aguarde ou cancele antes de criar outro.")
        
        # Verifica se o usuário existe
        from data.repo import usuario_repo
        usuario = usuario_repo.obter_por_id(request.cod_usuario)
        if not usuario:
            raise HTTPException(status_code=404, detail=f"Usuário com cod_usuario={request.cod_usuario} não encontrado no sistema.")
        
        # Busca a agenda para verificar disponibilidade
        agenda = agenda_repo.obter_por_id(request.cod_agenda)
        
        if not agenda:
            raise HTTPException(status_code=404, detail="Agenda não encontrada")
        
        sys.stderr.write(f"DEBUG - Agenda encontrada: cod_unidade={agenda.cod_unidade}\n")
        sys.stderr.flush()
        
        # Verifica se ainda há vagas disponíveis
        vagas_disponiveis = agenda.vagas - agenda.quantidade_doadores
        if vagas_disponiveis <= 0:
            raise HTTPException(status_code=400, detail="Não há mais vagas disponíveis para este horário")
        
        # Combina data e horário para criar datetime
        data_hora_str = f"{request.data} {request.horario}:00"
        data_hora = datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M:%S')
        
        # --- Validação do intervalo mínimo entre doações ---
        # Buscar última doação do usuário
        doacoes = doacao_repo.obter_doacoes_completas_por_doador(request.cod_usuario)
        ultima_doacao = None
        if doacoes:
            # Considera apenas doações com status concluído (status == 1)
            doacoes_concluidas = [d for d in doacoes if d.get('status') == 1 and d.get('data_hora')]
            if doacoes_concluidas:
                ultima_doacao = doacoes_concluidas[0]['data_hora']  # Ordenado por data desc
        
        if ultima_doacao:
            dias_entre = (data_hora.date() - ultima_doacao.date()).days
            genero = (usuario.genero or '').lower()
            if genero == 'masculino':
                intervalo_min = 60
            else:
                intervalo_min = 90
            if dias_entre < intervalo_min:
                raise HTTPException(
                    status_code=400,
                    detail=f"É necessário aguardar pelo menos {intervalo_min} dias entre doações. Última doação: {ultima_doacao.strftime('%d/%m/%Y')}.")
        
        # Cria o objeto Agendamento
        novo_agendamento = Agendamento(
            cod_agendamento=0,  # Será gerado pelo banco
            cod_usuario=request.cod_usuario,  # Alterado de cod_doador para cod_usuario
            data_hora=data_hora,
            status=0,  # 0 = não concluído
            tipo_agendamento='online',
            local_agendamento=agenda.cod_unidade,
            cod_colaborador=None  # NULL pois foi feito online pelo usuário
        )
        
        sys.stderr.write(f"DEBUG - Tentando inserir agendamento: cod_usuario={novo_agendamento.cod_usuario}, local={novo_agendamento.local_agendamento}\n")
        sys.stderr.flush()
        
        # Insere o agendamento
        cod_agendamento_criado = agendamento_repo.inserir(novo_agendamento)
        
        if not cod_agendamento_criado:
            raise HTTPException(status_code=500, detail="Erro ao criar agendamento")
        
        # Incrementa a quantidade de doadores na agenda
        sucesso_incremento = agenda_repo.incrementar_doadores(request.cod_agenda)
        
        if not sucesso_incremento:
            # Se falhar ao incrementar, tenta reverter o agendamento
            agendamento_repo.delete(cod_agendamento_criado)
            raise HTTPException(status_code=500, detail="Erro ao atualizar disponibilidade da agenda")
        
        return {
            "success": True,
            "message": "Agendamento criado com sucesso!",
            "cod_agendamento": cod_agendamento_criado,
            "data_hora": data_hora.strftime('%Y-%m-%d %H:%M'),
            "local": agenda.cod_unidade
        }
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Formato de data/hora inválido: {str(e)}")
    except Exception as e:
        import sys
        sys.stderr.write(f"DEBUG - Erro: {str(e)}\n")
        sys.stderr.flush()
        raise HTTPException(status_code=500, detail=f"Erro ao criar agendamento: {str(e)}")
