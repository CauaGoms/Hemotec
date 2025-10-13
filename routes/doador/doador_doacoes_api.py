from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from datetime import datetime
from util.auth_decorator import requer_autenticacao
from data.repo import doacao_repo, prontuario_repo, exame_repo

router = APIRouter()

@router.get("/api/doador/doacao/{cod_doacao}/detalhes")
@requer_autenticacao(["doador"])
async def get_detalhes_doacao(request: Request, cod_doacao: int, usuario_logado: dict = None):
    """
    Retorna os detalhes completos de uma doação específica, incluindo:
    - Dados da doação
    - Informações da unidade de coleta
    - Prontuário (se houver)
    - Exames (se houver)
    """
    try:
        # Verificar se a doação pertence ao usuário logado
        cod_doador = usuario_logado.get("cod_usuario")
        
        # Buscar doação completa
        doacoes = doacao_repo.obter_doacoes_completas_por_doador(cod_doador)
        doacao = next((d for d in doacoes if d['cod_doacao'] == cod_doacao), None)
        
        if not doacao:
            return JSONResponse(
                status_code=404,
                content={"erro": "Doação não encontrada"}
            )
        
        # Buscar prontuário relacionado à doação
        prontuario = prontuario_repo.obter_por_doacao(cod_doacao)
        
        # Buscar exames relacionados à doação
        exames = exame_repo.obter_por_doacao(cod_doacao)
        
        # Montar resposta com todos os dados
        detalhes = {
            "doacao": {
                "cod_doacao": doacao['cod_doacao'],
                "cod_agendamento": doacao['cod_agendamento'],
                "data_hora": doacao['data_hora'].isoformat() if doacao['data_hora'] else None,
                "quantidade": doacao['quantidade'],
                "status": doacao['status'],
                "observacoes": doacao['observacoes']
            },
            "doador": {
                "nome": doacao['nome_doador'],
                "tipo_sanguineo": doacao['tipo_sanguineo_completo']
            },
            "unidade": {
                "nome": doacao['nome_unidade'],
                "endereco_completo": doacao['endereco_completo'],
                "rua": doacao['rua_unidade'],
                "bairro": doacao['bairro_unidade'],
                "cidade": doacao['nome_cidade'],
                "estado": doacao['sigla_estado'],
                "cep": doacao['cep_unidade'],
                "telefone": doacao['telefone_unidade']
            },
            "prontuario": None,
            "exames": []
        }
        
        # Adicionar dados do prontuário se existir
        if prontuario:
            detalhes["prontuario"] = {
                "data_criacao": prontuario.data_criacao.isoformat() if prontuario.data_criacao else None,
                "jejum": prontuario.jejum,
                "diabetes": prontuario.diabetes,
                "hipertensao": prontuario.hipertensao,
                "cardiopatia": prontuario.cardiopatia,
                "cancer": prontuario.cancer,
                "hepatite": prontuario.hepatite,
                "sintomas_gripais": prontuario.sintomas_gripais,
                "medicamentos": prontuario.medicamentos,
                "detalhes_medicamentos": prontuario.detalhes_medicamentos,
                "fumante": prontuario.fumante,
                "alcool": prontuario.alcool
            }
        
        # Adicionar dados dos exames se existirem
        if exames:
            detalhes["exames"] = [
                {
                    "tipo_exame": exame.tipo_exame,
                    "resultado": exame.resultado,
                    "data_exame": exame.data_exame.isoformat() if isinstance(exame.data_exame, datetime) else str(exame.data_exame),
                    "arquivo": exame.arquivo
                }
                for exame in exames
            ]
        
        return JSONResponse(content=detalhes)
        
    except Exception as e:
        print(f"Erro ao buscar detalhes da doação: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"erro": "Erro ao buscar detalhes da doação"}
        )
