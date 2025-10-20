from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from data.repo import agendamento_repo, unidade_coleta_repo, doador_repo, usuario_repo
from util.auth_decorator import requer_autenticacao
import sys

router = APIRouter()

@router.get("/debug/agendamento/{id_agendamento}")
async def debug_agendamento(id_agendamento: int):
    agendamento = agendamento_repo.obter_por_id(id_agendamento)
    
    sys.stderr.write(f"\n[DEBUG API] agendamento = {agendamento}\n")
    sys.stderr.flush()
    
    data_hora_formatted = None
    error_msg = None
    
    if agendamento:
        sys.stderr.write(f"[DEBUG API] data_hora = {agendamento.data_hora} (type: {type(agendamento.data_hora)})\n")
        sys.stderr.flush()
        
        try:
            if agendamento.data_hora:
                # Teste simples
                data_hora_formatted_simple = agendamento.data_hora.strftime('%d/%m/%Y')
                sys.stderr.write(f"[DEBUG API] data_hora_formatted_simple = {data_hora_formatted_simple}\n")
                sys.stderr.flush()
                
                # Teste com hora
                data_hora_formatted_time = agendamento.data_hora.strftime('%H:%M')
                sys.stderr.write(f"[DEBUG API] data_hora_formatted_time = {data_hora_formatted_time}\n")
                sys.stderr.flush()
                
                # Teste com "às"
                data_hora_formatted = agendamento.data_hora.strftime('%d/%m/%Y às %H:%M')
                sys.stderr.write(f"[DEBUG API] data_hora_formatted = {data_hora_formatted}\n")
                sys.stderr.flush()
            else:
                error_msg = "data_hora is None"
                sys.stderr.write(f"[DEBUG API] ERROR: {error_msg}\n")
                sys.stderr.flush()
        except Exception as e:
            error_msg = f"Error formatting datetime: {str(e)}"
            sys.stderr.write(f"[DEBUG API] EXCEPTION: {error_msg}\n")
            sys.stderr.write(f"[DEBUG API] Exception traceback: {e.__traceback__}\n")
            sys.stderr.flush()
        
        return JSONResponse({
            "cod_agendamento": agendamento.cod_agendamento,
            "cod_colaborador": agendamento.cod_colaborador,
            "cod_usuario": agendamento.cod_usuario,
            "data_hora": str(agendamento.data_hora) if agendamento.data_hora else None,
            "data_hora_type": str(type(agendamento.data_hora)),
            "data_hora_formatted": data_hora_formatted,
            "error_formatting": error_msg,
            "status": agendamento.status,
            "tipo_agendamento": agendamento.tipo_agendamento,
            "local_agendamento": agendamento.local_agendamento
        })
    else:
        return JSONResponse({"error": "Agendamento not found"}, status_code=404)
