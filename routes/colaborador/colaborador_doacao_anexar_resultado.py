from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/doacao/anexar_resultado")
async def get_colaborador_doacao_anexar_resultado(request: Request):
    response = templates.TemplateResponse("colaborador/colaborador_doacao_anexar_resultado.html", {"request": request, "active_page": "doacao"})
    return response
