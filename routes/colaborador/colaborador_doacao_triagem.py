from fastapi import APIRouter, Request, Form, status
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from typing import Optional
from data.model.prontuario_model import Prontuario
from data.model.doador_model import Doador
from data.model.doacao_model import Doacao
import data.repo.prontuario_repo as prontuario_repo
import data.repo.doador_repo as doador_repo
import data.repo.doacao_repo as doacao_repo
import data.repo.usuario_repo as usuario_repo
from util.auth_decorator import obter_usuario_logado

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/doacao/triagem")
async def get_colaborador_doacao_triagem(request: Request):
    response = templates.TemplateResponse("colaborador/colaborador_doacao_triagem.html", {"request": request, "active_page": "doacoes"})
    return response

@router.get("/colaborador/doacao/triagem/{cod_doacao}")
async def get_colaborador_doacao_triagem_com_codigo(request: Request, cod_doacao: int):
    """Carrega a página de triagem com o código da doação"""
    try:
        # Obter a doação
        doacao = doacao_repo.obter_por_id(cod_doacao)
        if not doacao:
            # Redirecionar se não encontrar
            from fastapi.responses import RedirectResponse
            return RedirectResponse(url="/colaborador/doacoes", status_code=303)
        
        # Obter dados do doador
        doador = doador_repo.obter_por_id(doacao.cod_doador)
        usuario = usuario_repo.obter_por_id(doacao.cod_doador)
        
        response = templates.TemplateResponse(
            "colaborador/colaborador_doacao_triagem.html", 
            {
                "request": request, 
                "active_page": "doacoes",
                "cod_doacao": cod_doacao,
                "doacao": doacao,
                "doador": doador,
                "usuario": usuario
            }
        )
        return response
    except Exception as e:
        print(f"Erro ao carregar triagem: {e}")
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/colaborador/doacoes", status_code=303)

@router.post("/colaborador/doacao/triagem")
async def post_colaborador_doacao_triagem(
    request: Request,
    # Dados Pessoais e Físicos
    altura: float = Form(...),
    peso: float = Form(...),
    profissao: str = Form(...),
    contato_emergencia: str = Form(...),
    telefone_emergencia: str = Form(...),
    # Condições de Saúde
    jejum: str = Form(...),
    diabetes: str = Form(...),
    hipertensao: str = Form(...),
    cardiopatia: str = Form(...),
    cancer: str = Form(...),
    hepatite: str = Form(...),
    outras_condicoes: str = Form(...),
    outras_condicoes_texto: Optional[str] = Form(""),
    sintomas_gripais: str = Form(...),
    # Medicamentos
    medicamentos: str = Form(...),
    medicamentos_texto: Optional[str] = Form(""),
    # Estilo de Vida
    fumante: str = Form(...),
    alcool_12h: str = Form(...),
    drogas_ilicitas: str = Form(...),
    risco_ist: str = Form(...),
    atividade_fisica_12h: str = Form(...),
    sono_6h: str = Form(...),
    procedimentos_6m: str = Form(...),
    procedimentos_texto: Optional[str] = Form("")
):
    try:
        # TEMPORÁRIO: Usando cod_doador fixo até implementar autenticação completa
        # TODO: Remover isso quando a autenticação estiver funcionando
        cod_usuario = 12  # Usando doador fixo temporariamente
        
        # Obter o usuário logado da sessão (comentado temporariamente)
        # usuario_logado = obter_usuario_logado(request)
        # 
        # if not usuario_logado:
        #     return JSONResponse(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         content={"success": False, "message": "Usuário não autenticado"}
        #     )
        # 
        # # Obter o código do usuário (que é a chave primária na tabela usuario)
        # cod_usuario = usuario_logado.get('cod_usuario')
        # 
        # if not cod_usuario:
        #     return JSONResponse(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         content={"success": False, "message": "Código do usuário não encontrado na sessão"}
        #     )
        
        print(f"DEBUG: Buscando doador com cod_usuario = {cod_usuario}")
        
        # Buscar o doador usando o código do usuário
        # Na tabela doador, cod_doador é FK para usuario.cod_usuario
        doador = doador_repo.obter_por_id(cod_usuario)
        
        if not doador:
            print(f"DEBUG: Doador não encontrado para cod_usuario = {cod_usuario}")
            
            # Se não encontrar, tentar criar um registro básico de doador
            # Isso é necessário caso o usuário tenha sido criado mas não tenha registro de doador
            print(f"DEBUG: Tentando criar registro de doador para o usuário {cod_usuario}")
            
            usuario = usuario_repo.obter_por_id(cod_usuario)
            if not usuario:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"success": False, "message": "Usuário não encontrado"}
                )
            
            # Criar um novo doador com dados básicos
            novo_doador = Doador(
                cod_doador=cod_usuario,
                usuario=usuario,
                tipo_sanguineo="N/I",  # Não Informado
                fator_rh="N/I",
                elegivel="N",
                altura=altura,
                peso=peso,
                profissao=profissao,
                contato_emergencia=contato_emergencia,
                telefone_emergencia=telefone_emergencia
            )
            
            try:
                doador_repo.inserir(novo_doador)
                doador = doador_repo.obter_por_id(cod_usuario)
                print(f"DEBUG: Doador criado com sucesso: {doador.cod_doador}")
            except Exception as e_criar:
                print(f"DEBUG: Erro ao criar doador: {e_criar}")
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={"success": False, "message": f"Erro ao criar registro de doador: {str(e_criar)}"}
                )
        
        # Obter o código do doador (que é o mesmo que cod_usuario)
        cod_doador = doador.cod_doador
        print(f"DEBUG: cod_doador obtido = {cod_doador}")
        
        # Atualizar dados físicos do doador
        if doador:
            doador.altura = altura
            doador.peso = peso
            doador.profissao = profissao
            doador.contato_emergencia = contato_emergencia
            doador.telefone_emergencia = telefone_emergencia
            doador_repo.update(doador)
        
        # Avaliar se o doador está apto
        impedimentos = []
        
        # Verificar peso mínimo
        if peso < 50:
            impedimentos.append("Peso abaixo do mínimo (50kg)")
        
        # Verificar altura mínima
        if altura < 140:
            impedimentos.append("Altura abaixo do mínimo (140cm)")
        
        # Verificar condições de saúde impeditivas
        if diabetes == "sim":
            impedimentos.append("Diabetes")
        if cardiopatia == "sim":
            impedimentos.append("Cardiopatia")
        if cancer == "sim":
            impedimentos.append("Histórico de câncer")
        if hepatite == "sim":
            impedimentos.append("Hepatite")
        if sintomas_gripais == "sim":
            impedimentos.append("Sintomas gripais")
        
        # Verificar estilo de vida
        if alcool_12h == "sim":
            impedimentos.append("Consumo de álcool nas últimas 12 horas")
        if drogas_ilicitas == "sim":
            impedimentos.append("Uso de drogas ilícitas")
        if risco_ist == "sim":
            impedimentos.append("Situação de risco para IST")
        if atividade_fisica_12h == "sim":
            impedimentos.append("Atividade física intensa nas últimas 12 horas")
        if sono_6h == "nao":
            impedimentos.append("Sono insuficiente (menos de 6 horas)")
        if procedimentos_6m == "sim":
            impedimentos.append("Procedimentos recentes (tatuagem, piercing, etc.)")
        
        # Determinar se está apto
        apto = len(impedimentos) == 0
        
        # Debug: Verificar o código do doador antes de criar a doação
        print(f"DEBUG: cod_doador = {cod_doador}")
        print(f"DEBUG: Criando doação para doador {cod_doador}")
        
        # Criar doação pendente (status 0 = pendente, 1 = realizada)
        doacao = Doacao(
            cod_doacao=0,  # Será gerado pelo banco
            cod_doador=cod_doador,
            cod_agendamento=None,  # Pode ser preenchido posteriormente ao vincular com um agendamento
            data_hora=datetime.now(),
            quantidade=0,  # Quantidade padrão de uma doação em ml
            status=0  # Pendente
        )
        
        try:
            cod_doacao = doacao_repo.inserir(doacao)
            print(f"DEBUG: Doação criada com código {cod_doacao}")
        except Exception as e_doacao:
            print(f"DEBUG: Erro ao inserir doação: {e_doacao}")
            print(f"DEBUG: Tentando verificar se o doador existe...")
            # Verificar se o doador realmente existe
            doador_teste = doador_repo.obter_por_id(cod_doador)
            print(f"DEBUG: Doador encontrado: {doador_teste is not None}")
            raise
        
        if not cod_doacao:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"success": False, "message": "Erro ao criar registro de doação"}
            )
        
        # Criar prontuário com os dados da triagem
        prontuario = Prontuario(
            cod_prontuario=0,  # Será gerado pelo banco
            cod_doacao=cod_doacao,
            data_criacao=datetime.now(),
            data_atualizacao=datetime.now(),
            jejum=(jejum == "sim"),
            diabetes=(diabetes == "sim"),
            hipertensao=(hipertensao == "sim"),
            cardiopatia=(cardiopatia == "sim"),
            cancer=(cancer == "sim"),
            hepatite=(hepatite == "sim"),
            outros=(outras_condicoes == "sim"),
            detalhes_outros=outras_condicoes_texto or "",
            sintomas_gripais=(sintomas_gripais == "sim"),
            medicamentos=(medicamentos == "sim"),
            detalhes_medicamentos=medicamentos_texto or "",
            fumante=(fumante == "sim"),
            alcool=(alcool_12h == "sim"),
            droga=(drogas_ilicitas == "sim"),
            ist=(risco_ist == "sim"),
            atividade=(atividade_fisica_12h == "sim"),
            sono=(sono_6h == "sim"),
            tatuagem_e_outros=(procedimentos_6m == "sim")
        )
        
        cod_prontuario = prontuario_repo.inserir(prontuario)
        
        if not cod_prontuario:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"success": False, "message": "Erro ao salvar prontuário"}
            )
        
        # Atualizar elegibilidade do doador
        if doador:
            doador.elegivel = "S" if apto else "N"
            doador_repo.update(doador)
        
        # Retornar resultado
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "apto": apto,
                "impedimentos": impedimentos,
                "cod_doacao": cod_doacao,
                "cod_prontuario": cod_prontuario,
                "message": "Triagem realizada com sucesso!" if apto else "Triagem realizada. Você possui impedimentos temporários ou permanentes."
            }
        )
        
    except Exception as e:
        print(f"Erro ao processar triagem: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "message": f"Erro ao processar triagem: {str(e)}"}
        )
