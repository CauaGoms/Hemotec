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

# Importando os routers públicos
from routes.publico.api_public import router as public_router
from routes.publico.login import router as login_router
from routes.publico.login_cadastro import router as cadastro_router
from routes.publico.login_esqueceu_senha import router as login_esqueceu_senha_router
from routes.publico.sobre import router as sobre_router
from routes.publico.campanha import router as campanha_router
from routes.publico.contato import router as contato_router

# Importando os routers do doador
from routes.doador.doador import router as doador_router
from routes.doador.doador_campanha import router as doador_campanha_router
from routes.doador.doador_agendamento import router as doador_agendamento_router
from routes.doador.doador_agendamento_confirmar import router as doador_agendamento_confirmar_router
from routes.doador.doador_agendamento_historico_agendamentos import router as doador_agendamento_historico_router
from routes.doador.doador_notificacao import router as doador_notificacao_router
from routes.doador.doador_meu_perfil import router as doador_meu_perfil_router
from routes.doador.doador_configuracoes import router as doador_configuracoes_router
from routes.doador.doador_novo_doador import router as doador_novo_doador_router
from routes.doador.doador_reagendamento import router as doador_reagendamento_router
from routes.doador.doador_sair import router as doador_sair_router
from routes.doador.doador_estoque import router as doador_estoque_router
from routes.doador.doador_carteira import router as doador_carteira_router

# Importando os routers do administrador de unidade de coleta
from routes.adm_unidade.administrador import router as administrador_router
from routes.adm_unidade.administrador_relatorios import router as administrador_relatorios_router
from routes.adm_unidade.administrador_relatorios_por_tipo_sanguineo import router as administrador_relatorios_por_tipo_sanguineo_router
from routes.adm_unidade.administrador_relatorios_por_periodo import router as administrador_relatorios_por_periodo_router
from routes.adm_unidade.administrador_notificacao import router as administrador_notificacao_router
from routes.adm_unidade.administrador_colaboradores import router as administrador_colaboradores_router
from routes.adm_unidade.administrador_colaboradores_excluir import router as administrador_colaboradores_excluir_router
from routes.adm_unidade.administrador_colaboradores_detalhes import router as administrador_colaboradores_detalhes_router
from routes.adm_unidade.administrador_colaboradores_alterar import router as administrador_colaboradores_alterar_router
from routes.adm_unidade.administrador_colaboradores_adicionar import router as administrador_colaboradores_adicionar_router
from routes.adm_unidade.administrador_campanha import router as administrador_campanha_router
from routes.adm_unidade.administrador_campanha_excluir import router as administrador_campanha_excluir_router
from routes.adm_unidade.administrador_campanha_detalhes import router as administrador_campanha_detalhes_router
from routes.adm_unidade.administrador_campanha_alterar import router as administrador_campanha_alterar_router
from routes.adm_unidade.administrador_campanha_adicionar import router as administrador_campanha_adicionar_router

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

app.include_router(public_router)
app.include_router(login_router)
app.include_router(cadastro_router)
app.include_router(login_esqueceu_senha_router)
app.include_router(sobre_router)
app.include_router(campanha_router)
app.include_router(contato_router)

app.include_router(doador_router)
app.include_router(doador_campanha_router)
app.include_router(doador_agendamento_router)
app.include_router(doador_agendamento_confirmar_router)
app.include_router(doador_agendamento_historico_router)
app.include_router(doador_notificacao_router)
app.include_router(doador_meu_perfil_router)
app.include_router(doador_configuracoes_router)
app.include_router(doador_novo_doador_router)
app.include_router(doador_reagendamento_router)
app.include_router(doador_sair_router)
app.include_router(doador_estoque_router)
app.include_router(doador_carteira_router)

app.include_router(administrador_router)
app.include_router(administrador_relatorios_router)
app.include_router(administrador_relatorios_por_tipo_sanguineo_router)
app.include_router(administrador_relatorios_por_periodo_router)
app.include_router(administrador_notificacao_router)
app.include_router(administrador_colaboradores_router)
app.include_router(administrador_colaboradores_excluir_router)
app.include_router(administrador_colaboradores_detalhes_router)
app.include_router(administrador_colaboradores_alterar_router)
app.include_router(administrador_colaboradores_adicionar_router)
app.include_router(administrador_campanha_router)
app.include_router(administrador_campanha_excluir_router)
app.include_router(administrador_campanha_detalhes_router)
app.include_router(administrador_campanha_alterar_router)
app.include_router(administrador_campanha_adicionar_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)