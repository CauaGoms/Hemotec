from datetime import datetime, date
from typing import Optional

def calcular_intervalo_doacao(genero: str, ultima_doacao_data: Optional[date]) -> dict:
    """
    Calcula o intervalo entre doações e verifica se o doador pode doar novamente.
    
    Args:
        genero: 'Masculino', 'Feminino' ou 'Outros'
        ultima_doacao_data: Data da última doação (date object) ou None se nunca doou
        
    Returns:
        dict com informações sobre o intervalo:
        {
            'pode_doar': bool,
            'dias_desde_ultima': int ou None,
            'dias_minimos': int,
            'dias_restantes': int ou 0,
            'proxima_doacao': date ou None,
            'mensagem': str,
            'status': 'apto' | 'aguardando' | 'nunca_doou'
        }
    """
    # Define intervalo mínimo baseado no gênero
    if genero == 'Masculino':
        dias_minimos = 60
    elif genero == 'Feminino':
        dias_minimos = 90
    else:  # 'Outros'
        dias_minimos = 90  # Usa o intervalo mais conservador
    
    # Se nunca doou
    if ultima_doacao_data is None:
        return {
            'pode_doar': True,
            'dias_desde_ultima': None,
            'dias_minimos': dias_minimos,
            'dias_restantes': 0,
            'proxima_doacao': None,
            'mensagem': 'Você nunca doou sangue. Está apto para fazer sua primeira doação!',
            'status': 'nunca_doou'
        }
    
    # Calcula dias desde a última doação
    hoje = date.today()
    
    # Converte datetime para date se necessário
    if isinstance(ultima_doacao_data, datetime):
        ultima_doacao_data = ultima_doacao_data.date()
    
    dias_desde_ultima = (hoje - ultima_doacao_data).days
    
    # Calcula próxima data disponível
    from datetime import timedelta
    proxima_doacao = ultima_doacao_data + timedelta(days=dias_minimos)
    
    # Verifica se pode doar
    pode_doar = dias_desde_ultima >= dias_minimos
    dias_restantes = max(0, dias_minimos - dias_desde_ultima)
    
    if pode_doar:
        mensagem = f'Você está apto para doar! Já se passaram {dias_desde_ultima} dias desde sua última doação.'
        status = 'apto'
    else:
        mensagem = f'Aguarde mais {dias_restantes} dias para poder doar novamente. Última doação há {dias_desde_ultima} dias.'
        status = 'aguardando'
    
    return {
        'pode_doar': pode_doar,
        'dias_desde_ultima': dias_desde_ultima,
        'dias_minimos': dias_minimos,
        'dias_restantes': dias_restantes,
        'proxima_doacao': proxima_doacao,
        'mensagem': mensagem,
        'status': status,
        'ultima_doacao': ultima_doacao_data
    }


def obter_ultima_doacao_doador(cod_doador: int):
    """
    Busca a data da última doação de um doador.
    
    Args:
        cod_doador: Código do doador
        
    Returns:
        date da última doação ou None se nunca doou
    """
    from data.repo import doacao_repo
    
    doacoes = doacao_repo.obter_doacoes_completas_por_doador(cod_doador)
    
    if not doacoes:
        return None
    
    # Pega a doação mais recente
    # Assumindo que doacoes vem ordenado ou ordenamos aqui
    datas = []
    for doacao in doacoes:
        data_hora = doacao.get('data_hora')
        if data_hora:
            if isinstance(data_hora, str):
                # Parse string para date
                try:
                    data_obj = datetime.strptime(data_hora, '%Y-%m-%d').date()
                    datas.append(data_obj)
                except:
                    try:
                        data_obj = datetime.strptime(data_hora, '%Y-%m-%d %H:%M:%S').date()
                        datas.append(data_obj)
                    except:
                        pass
            elif isinstance(data_hora, (date, datetime)):
                if isinstance(data_hora, datetime):
                    datas.append(data_hora.date())
                else:
                    datas.append(data_hora)
    
    if datas:
        return max(datas)  # Retorna a data mais recente
    
    return None
