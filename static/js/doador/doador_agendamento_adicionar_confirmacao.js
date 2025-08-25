document.addEventListener('DOMContentLoaded', function() {
    // Função para buscar parâmetros da URL
    const getUrlParameter = (name) => {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        const regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        const results = regex.exec(location.search);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    };

    // Tenta obter dados da URL. Se não houver, usa dados de exemplo.
    const locationName = getUrlParameter('location') || 'Hemocentro Regional de Cachoeiro';
    const address = getUrlParameter('address') || 'Rua Dr. Raulino de Oliveira, 345 - Centro';
    const date = getUrlParameter('date') || 'Sexta-feira, 27 de Junho de 2025';
    const time = getUrlParameter('time') || '10:30';

    // Seleciona os elementos da página de confirmação
    const confirmLocationEl = document.getElementById('confirm-location');
    const confirmAddressEl = document.getElementById('confirm-address');
    const confirmDateTimeEl = document.getElementById('confirm-datetime');

    // Preenche os elementos com os dados do agendamento
    if (confirmLocationEl) {
        confirmLocationEl.textContent = locationName;
    }
    if (confirmAddressEl) {
        confirmAddressEl.textContent = address;
    }
    if (confirmDateTimeEl) {
        confirmDateTimeEl.textContent = `${date} às ${time}`;
    }

    // Adiciona a classe 'visible' para iniciar a animação de fade-in
    const confirmationContainer = document.querySelector('.confirmation-container');
    if (confirmationContainer) {
        // Um pequeno atraso para garantir que a página esteja pronta para a transição
        setTimeout(() => {
            confirmationContainer.classList.add('visible');
        }, 100);
    }
});
