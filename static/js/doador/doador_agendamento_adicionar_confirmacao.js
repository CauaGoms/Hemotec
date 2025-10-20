document.addEventListener('DOMContentLoaded', async function () {
    // Função para buscar parâmetros da URL
    const getUrlParameter = (name) => {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        const regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        const results = regex.exec(location.search);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    };

    // Obtém os dados necessários da URL
    const codUnidade = getUrlParameter('unidade');
    const codAgenda = getUrlParameter('cod_agenda');
    const data = getUrlParameter('data');
    const horario = getUrlParameter('horario');

    // Verifica se todos os parâmetros estão presentes
    if (!codUnidade || !codAgenda || !data || !horario) {
        alert('Dados do agendamento incompletos. Por favor, tente novamente.');
        window.location.href = '/doador/agendamento/adicionar';
        return;
    }

    // Verifica se o cod_doador foi passado pelo template
    if (!window.COD_DOADOR) {
        alert('Erro: usuário não identificado. Por favor, faça login novamente.');
        window.location.href = '/doador/agendamento/adicionar';
        return;
    }

    try {
        const codUsuario = window.COD_DOADOR;  // Na verdade é cod_usuario

        // Cria o agendamento via API
        const response = await fetch('/api/doador/agendamento/criar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                cod_usuario: codUsuario,  // Alterado de cod_doador para cod_usuario
                cod_agenda: parseInt(codAgenda),
                data: data,
                horario: horario
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'Erro ao criar agendamento');
        }

        // Se chegou aqui, o agendamento foi criado com sucesso
        console.log('Agendamento criado com sucesso:', result);

        // Busca informações da unidade para exibir
        const unidadeResponse = await fetch(`/api/publico/unidade/${codUnidade}`);
        let locationName = 'Hemocentro';
        let address = '';

        if (unidadeResponse.ok) {
            const unidade = await unidadeResponse.json();
            locationName = unidade.nome || 'Hemocentro';
            address = `${unidade.rua_unidade || ''} - ${unidade.bairro_unidade || ''}`;
        }

        // Formata a data para exibição
        const [ano, mes, dia] = data.split('-');
        const dataObj = new Date(ano, mes - 1, dia);
        const diasSemana = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'];
        const meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
        const dataFormatada = `${diasSemana[dataObj.getDay()]}, ${dia} de ${meses[dataObj.getMonth()]} de ${ano}`;

        // Atualiza os elementos da página com os dados
        const confirmLocationEl = document.getElementById('confirm-location');
        const confirmAddressEl = document.getElementById('confirm-address');
        const confirmDateTimeEl = document.getElementById('confirm-datetime');

        if (confirmLocationEl) {
            confirmLocationEl.textContent = locationName;
        }
        if (confirmAddressEl) {
            confirmAddressEl.textContent = address;
        }
        if (confirmDateTimeEl) {
            confirmDateTimeEl.textContent = `${dataFormatada} às ${horario}`;
        }

        // Adiciona a classe 'visible' para iniciar a animação de fade-in
        const confirmationContainer = document.querySelector('.confirmation-container');
        if (confirmationContainer) {
            setTimeout(() => {
                confirmationContainer.classList.add('visible');
            }, 100);
        }

    } catch (error) {
        console.error('Erro ao processar agendamento:', error);
        alert(`Erro ao confirmar agendamento: ${error.message}. Tente novamente.`);
        window.location.href = '/doador/agendamento/adicionar';
    }
});
