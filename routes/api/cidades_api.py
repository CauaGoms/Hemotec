from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/api/cidades")
async def get_cidades():
    """Retorna todas as cidades para preenchimento automático"""
    from data.repo import cidade_repo
    
    try:
        cidades = cidade_repo.obter_todos()
        
        # Converter para dict
        cidades_dict = []
        for cidade in cidades:
            cidades_dict.append({
                "cod_cidade": cidade.cod_cidade,
                "nome_cidade": cidade.nome_cidade,
                "sigla_estado": cidade.sigla_estado
            })
        
        return JSONResponse(content=cidades_dict)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )
