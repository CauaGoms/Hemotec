from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from data.repo import unidade_coleta_repo
from typing import Dict, Any

from data.repo import estoque_repo

def calcular_nivel_estoque(quantidade: int) -> Dict[str, Any]:
    # Use thresholds defined per bags (bolsas):
    # <= 59 -> Crítico
    # 60 - 99 -> Baixo
    # 100 - 149 -> Moderado
    # >= 150 -> Adequado
    # porcentagem is a fraction between 0 and 1 relative to an ideal maximum (170 bolsas)
    maximo_ideal = 170
    porcentagem = min(quantidade / maximo_ideal, 1)
    if quantidade <= 59:
        return {"status": "Crítico", "classe": "bg-danger", "porcentagem": porcentagem}
    elif quantidade <= 99:
        return {"status": "Baixo", "classe": "bg-warning", "porcentagem": porcentagem}
    elif quantidade <= 149:
        return {"status": "Moderado", "classe": "bg-info", "porcentagem": porcentagem}
    else:
        return {"status": "Adequado", "classe": "bg-success", "porcentagem": porcentagem}


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/api/unidades")
async def get_api_unidades():
    """
    Esta é uma rota de API. Ela não retorna HTML.
    Ela retorna apenas os dados das unidades de coleta em formato JSON.
    """
    coordenadas = unidade_coleta_repo.obter_coordenada() or []
    return coordenadas

@router.get("/api/estoque/{cod_unidade}")
async def get_api_estoque_unidade(cod_unidade: int):
    """
    API para buscar estoque de uma unidade específica
    """
    try:
        # Busca o estoque da unidade no banco de dados
        estoque_lista = estoque_repo.obter_por_unidade(cod_unidade)
        
        if not estoque_lista:
            return {
                "cod_unidade": cod_unidade,
                "estoque": {},
                "success": True,
                "message": "Nenhum estoque encontrado para esta unidade"
            }
        
        # Organiza os dados por tipo sanguíneo
        estoque_organizado = {}
        for item in estoque_lista:
            # Formatar tipo sanguíneo corretamente
            fator_simbolo = "+" if item.fator_rh and item.fator_rh.lower() == "positivo" else "-"
            tipo_completo = f"{item.tipo_sanguineo}{fator_simbolo}"
            nivel_info = calcular_nivel_estoque(item.quantidade)
            
            estoque_organizado[tipo_completo] = {
                "quantidade": item.quantidade,
                "status": nivel_info["status"],
                "classe": nivel_info["classe"],
                "porcentagem": nivel_info["porcentagem"],
                "data_atualizacao": item.data_atualizacao.isoformat() if item.data_atualizacao else None
            }
        
        return {
            "cod_unidade": cod_unidade,
            "estoque": estoque_organizado,
            "success": True
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "success": False
        }


@router.get("/api/publico/usuario-info")
async def get_usuario_info(request: Request):
    """
    API para obter informações do usuário logado da sessão
    """
    try:
        usuario_logado = request.session.get("usuario_logado")
        
        if not usuario_logado:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        return {
            "success": True,
            "cod_usuario": usuario_logado.get("cod_usuario"),
            "nome": usuario_logado.get("nome"),
            "tipo_usuario": usuario_logado.get("tipo_usuario")
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter informações do usuário: {str(e)}")


@router.get("/api/publico/unidade/{cod_unidade}")
async def get_unidade_info(cod_unidade: int):
    """
    API para obter informações de uma unidade de coleta específica
    """
    try:
        unidade = unidade_coleta_repo.obter_por_id(cod_unidade)
        
        if not unidade:
            raise HTTPException(status_code=404, detail="Unidade não encontrada")
        
        return {
            "success": True,
            "cod_unidade": unidade.cod_unidade,
            "nome": unidade.nome,
            "rua_unidade": unidade.rua_unidade,
            "bairro_unidade": unidade.bairro_unidade,
            "cep_unidade": unidade.cep_unidade,
            "telefone": unidade.telefone,
            "latitude": unidade.latitude,
            "longitude": unidade.longitude
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter informações da unidade: {str(e)}")
