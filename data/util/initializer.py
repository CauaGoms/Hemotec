from util.database import get_connection as obter_conexao
from repo import usuario_repo, adm_campanha_repo, adm_unidade_repo, agendamento_repo, assinatura_repo, campanha_repo, cidade_repo, colaborador_repo, doacao_repo, doador_repo, estoque_repo, exame_repo, gestor_repo, instituicao_repo, licenca_repo, notificacao_repo, plano_repo, prontuario_repo, unidade_coleta_repo 

def criar_tabelas():
    usuario_repo.criar_tabela()
    adm_campanha_repo.criar_tabela()
    adm_unidade_repo.criar_tabela()
    agendamento_repo.criar_tabela()
    assinatura_repo.criar_tabela()
    campanha_repo.criar_tabela()
    cidade_repo.criar_tabela()
    colaborador_repo.criar_tabela()
    doacao_repo.criar_tabela()
    doador_repo.criar_tabela()
    estoque_repo.criar_tabela()
    exame_repo.criar_tabela()
    gestor_repo.criar_tabela()
    instituicao_repo.criar_tabela()
    licenca_repo.criar_tabela()
    notificacao_repo.criar_tabela()
    plano_repo.criar_tabela()
    prontuario_repo.criar_tabela()
    unidade_coleta_repo.criar_tabela()

def inserir_dados_iniciais():
    # Obtém a conexão com o banco de dados
    conexao = obter_conexao()
    # Insere dados iniciais nas tabelas usando a mesma conexão para evitar problemas de concorrência
    usuario_repo.inserir_dados_iniciais(conexao)
    adm_campanha_repo.inserir_dados_iniciais(conexao)
    adm_unidade_repo.inserir_dados_iniciais(conexao)
    agendamento_repo.inserir_dados_iniciais(conexao)
    assinatura_repo.inserir_dados_iniciais(conexao)
    campanha_repo.inserir_dados_iniciais(conexao)
    cidade_repo.inserir_dados_iniciais(conexao)
    colaborador_repo.inserir_dados_iniciais(conexao)
    doacao_repo.inserir_dados_iniciais(conexao)
    doador_repo.inserir_dados_iniciais(conexao)
    estoque_repo.inserir_dados_iniciais(conexao)
    exame_repo.inserir_dados_iniciais(conexao)
    gestor_repo.inserir_dados_iniciais(conexao)
    instituicao_repo.inserir_dados_iniciais(conexao)
    licenca_repo.inserir_dados_iniciais(conexao)
    notificacao_repo.inserir_dados_iniciais(conexao)
    plano_repo.inserir_dados_iniciais(conexao)
    prontuario_repo.inserir_dados_iniciais(conexao)
    unidade_coleta_repo.inserir_dados_iniciais(conexao)
    # Commit para garantir que as alterações sejam salvas
    conexao.commit()
    # Fecha a conexão após inserir os dados
    conexao.close()