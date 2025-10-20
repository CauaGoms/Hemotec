from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from data.repo import unidade_coleta_repo, usuario_repo, doador_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/agendamento/adicionar")
@requer_autenticacao(["colaborador"])
async def get_colaborador_agendamento_adicionar(request: Request, usuario_logado: dict = None):
    # Buscar todas as unidades de coleta do banco de dados
    unidades = unidade_coleta_repo.obter_todos() or []
    
    response = templates.TemplateResponse(
        "colaborador/colaborador_agendamento_adicionar.html", 
        {
            "request": request, 
            "active_page": "agendamento", 
            "usuario": usuario_logado,
            "unidades": unidades
        }
    )
    return response

@router.get("/api/colaborador/buscar-doadores")
@requer_autenticacao(["colaborador"])
async def buscar_doadores(query: str = Query(...), usuario_logado: dict = None):
    """
    Busca doadores por nome ou CPF
    """
    try:
        if not query or len(query.strip()) < 2:
            return JSONResponse(content={
                "success": False,
                "message": "Digite pelo menos 2 caracteres"
            }, status_code=400)
        
        query_lower = query.lower().strip()
        
        # Buscar todos os usuários com perfil doador
        try:
            usuarios = usuario_repo.obter_todos() or []
        except Exception as e:
            import sys
            sys.stderr.write(f"Erro ao obter usuarios: {str(e)}\n")
            sys.stderr.flush()
            return JSONResponse(content={
                "success": False,
                "message": f"Erro ao buscar usuários: {str(e)}"
            }, status_code=500)
        
        doadores_encontrados = []
        
        for usuario in usuarios:
            try:
                # Verificar se é doador - handle None perfil
                if not usuario.perfil or usuario.perfil.strip().lower() != 'doador':
                    continue
                
                # Buscar por nome (parcial)
                nome_lower = usuario.nome.lower() if usuario.nome else ""
                if query_lower in nome_lower:
                    # Verificar se tem registro em doador
                    try:
                        doador = doador_repo.obter_por_id(usuario.cod_usuario)
                    except:
                        doador = None
                    
                    doadores_encontrados.append({
                        "cod_usuario": usuario.cod_usuario,
                        "nome": usuario.nome or "",
                        "cpf": usuario.cpf or "",
                        "email": usuario.email or "",
                        "telefone": usuario.telefone or "",
                        "is_doador": doador is not None
                    })
                # Buscar por CPF (apenas números)
                elif usuario.cpf:
                    cpf_apenas_numeros = ''.join(c for c in usuario.cpf if c.isdigit())
                    query_apenas_numeros = ''.join(c for c in query_lower if c.isdigit())
                    if query_apenas_numeros and query_apenas_numeros in cpf_apenas_numeros:
                        try:
                            doador = doador_repo.obter_por_id(usuario.cod_usuario)
                        except:
                            doador = None
                        
                        doadores_encontrados.append({
                            "cod_usuario": usuario.cod_usuario,
                            "nome": usuario.nome or "",
                            "cpf": usuario.cpf or "",
                            "email": usuario.email or "",
                            "telefone": usuario.telefone or "",
                            "is_doador": doador is not None
                        })
            except Exception as usuario_error:
                import sys
                sys.stderr.write(f"Erro ao processar usuario {usuario.cod_usuario if hasattr(usuario, 'cod_usuario') else 'desconhecido'}: {str(usuario_error)}\n")
                sys.stderr.flush()
                continue
        
        return JSONResponse(content={
            "success": True,
            "doadores": doadores_encontrados[:20]  # Limitar a 20 resultados
        })
        
    except Exception as e:
        import sys
        sys.stderr.write(f"Erro na busca de doadores: {str(e)}\n")
        sys.stderr.flush()
        return JSONResponse(content={
            "success": False,
            "message": f"Erro ao buscar doadores: {str(e)}"
        }, status_code=500)