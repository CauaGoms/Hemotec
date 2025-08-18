from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

from data.repo import cidade_repo
from data.repo import campanha_repo
from data.repo import usuario_repo
from data.repo import gestor_repo
from data.repo import instituicao_repo
from data.repo import assinatura_repo
from data.repo import plano_repo
from data.repo import licenca_repo
from data.repo import adm_unidade_repo
from data.repo import adm_campanha_repo
from data.repo import unidade_coleta_repo
from data.repo import estoque_repo
from data.repo import notificacao_repo
from data.repo import colaborador_repo
from data.repo import agendamento_repo
from data.repo import doador_repo
from data.repo import doacao_repo
from data.repo import exame_repo
from data.repo import prontuario_repo


# Importando os routers do colaborador
from routes.colaborador.colaborador import router as colaborador_router
from routes.colaborador.colaborador_campanha import router as colaborador_campanha_router
from routes.colaborador.colaborador_campanha_adicionar import router as colaborador_campanha_adicionar_router
from routes.colaborador.colaborador_campanha_alterar import router as colaborador_campanha_alterar_router
from routes.colaborador.colaborador_campanha_excluir import router as colaborador_campanha_excluir_router
from routes.colaborador.colaborador_campanha_detalhe import router as colaborador_campanha_detalhe_router
from routes.colaborador.colaborador_notificacao import router as colaborador_notificacao_router
from routes.colaborador.colaborador_agendamento import router as colaborador_agendamento_router
from routes.colaborador.colaborador_agendamento_adicionar import router as colaborador_agendamento_adicionar_router
from routes.colaborador.colaborador_agendamento_alterar import router as colaborador_agendamento_alterar_router
from routes.colaborador.colaborador_agendamento_excluir import router as colaborador_agendamento_excluir_router
from routes.colaborador.colaborador_doacao import router as colaborador_doacao_router
from routes.colaborador.colaborador_doacao_adicionar import router as colaborador_doacao_adicionar_router
from routes.colaborador.colaborador_doacao_alterar import router as colaborador_doacao_alterar_router
from routes.colaborador.colaborador_doacao_excluir import router as colaborador_doacao_excluir_router
from routes.colaborador.colaborador_doacao_detalhe import router as colaborador_doacao_detalhe_router
from routes.colaborador.colaborador_doacao_anexar_resultado import router as colaborador_doacao_anexar_resultado_router
from routes.colaborador.colaborador_disponibilidade_coleta import router as colaborador_disponibilidade_coleta_router

# Importando os routers do usuario
from routes.usuario.usuario_alterar_senha import router as usuario_alterar_senha_router
from routes.usuario.usuario_sair import router as usuario_sair_router



app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-here")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

cidade_repo.criar_tabela()
usuario_repo.criar_tabela()
campanha_repo.criar_tabela()
plano_repo.criar_tabela()
instituicao_repo.criar_tabela()
gestor_repo.criar_tabela()
assinatura_repo.criar_tabela()
licenca_repo.criar_tabela()
unidade_coleta_repo.criar_tabela()
estoque_repo.criar_tabela()
adm_unidade_repo.criar_tabela()
adm_campanha_repo.criar_tabela()
notificacao_repo.criar_tabela()
colaborador_repo.criar_tabela()
doador_repo.criar_tabela()
agendamento_repo.criar_tabela()
doacao_repo.criar_tabela()
exame_repo.criar_tabela()
prontuario_repo.criar_tabela()

#routers do colaborador
app.include_router(colaborador_router)
app.include_router(colaborador_campanha_router)
app.include_router(colaborador_campanha_adicionar_router)
app.include_router(colaborador_campanha_alterar_router)
app.include_router(colaborador_campanha_excluir_router)
app.include_router(colaborador_campanha_detalhe_router)
app.include_router(colaborador_notificacao_router)
app.include_router(colaborador_agendamento_router)
app.include_router(colaborador_agendamento_adicionar_router)
app.include_router(colaborador_agendamento_alterar_router)
app.include_router(colaborador_agendamento_excluir_router)
app.include_router(colaborador_doacao_router)
app.include_router(colaborador_doacao_adicionar_router)
app.include_router(colaborador_doacao_alterar_router)
app.include_router(colaborador_doacao_excluir_router)
app.include_router(colaborador_doacao_detalhe_router)
app.include_router(colaborador_doacao_anexar_resultado_router)
app.include_router(colaborador_disponibilidade_coleta_router)


#routers do usuario
app.include_router(usuario_alterar_senha_router)
app.include_router(usuario_sair_router)

##routers do adm_unidade


#routers do gestor


#routers do usuario


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)