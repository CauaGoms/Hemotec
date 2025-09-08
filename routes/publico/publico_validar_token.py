from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/validar_token")
async def get_validar_token(request: Request):
    response = templates.TemplateResponse("publico/publico_validar_token.html", {"request": request})
    return response

@router.post("/validar_token")
async def post_validar_token(request: Request):
    return templates.TemplateResponse("publico/publico_validar_token.html", {"request": request})