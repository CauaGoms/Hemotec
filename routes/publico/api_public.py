from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.repo import unidade_coleta_repo
from typing import Dict, Any

from data.repo import estoque_repo

def calcular_nivel_estoque(quantidade: int) -> Dict[str, Any]:
    maximo_ideal = 10000
    porcentagem = min((quantidade / maximo_ideal) * 100, 100)
    if quantidade <= 2000:
        return {"status": "Crítico", "classe": "bg-danger", "porcentagem": porcentagem}
    elif quantidade <= 5000:
        return {"status": "Baixo", "classe": "bg-warning", "porcentagem": porcentagem}
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
            tipo_completo = f"{item.tipo_sanguineo}{item.fator_rh}"
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