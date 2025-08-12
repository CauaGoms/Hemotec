// Salve como /static/js/estoque_publico.js
document.addEventListener('DOMContentLoaded', function () {
    const emptyState = document.getElementById('emptyState');
    const loadingState = document.getElementById('loadingState');
    const stockPanel = document.getElementById('stockPanel');
    const stockLevelsContainer = document.getElementById('stock-levels');
    const hemocentroTitle = document.getElementById('stock-hemocentro-title');
    const alertMessage = document.getElementById('alert-message');
    const searchInput = document.getElementById('search-input');
    const locationCards = document.querySelectorAll('.location-card');

    // Dados de estoque simulados (baseados em boas_vindas_inicio.html)
    const mockStockData = {
        1: { 'O+': 20, 'A+': 35, 'B+': 70, 'AB+': 30, 'O-': 45, 'A-': 65, 'B-': 25, 'AB-': 80 },
        2: { 'O+': 80, 'A+': 75, 'B+': 60, 'AB+': 85, 'O-': 70, 'A-': 90, 'B-': 55, 'AB-': 95 },
        3: { 'O+': 30, 'A+': 25, 'B+': 40, 'AB+': 50, 'O-': 20, 'A-': 35, 'B-': 45, 'AB-': 60 }
    };

    function getStockStatus(percentage) {
        if (percentage <= 25) return { text: 'Crítico', class: 'bg-danger' };
        if (percentage <= 40) return { text: 'Baixo', class: 'bg-warning text-dark' };
        if (percentage <= 60) return { text: 'Moderado', class: 'bg-info text-dark' };
        return { text: 'Adequado', class: 'bg-success' };
    }

    function displayStock(locationId, locationName) {
        const data = mockStockData[locationId];
        hemocentroTitle.textContent = `Estoque - ${locationName}`;
        stockLevelsContainer.innerHTML = '';
        let urgentTypes = [];

        Object.keys(data).forEach(type => {
            const percentage = data[type];
            const status = getStockStatus(percentage);
            if (status.text === 'Crítico' || status.text === 'Baixo') {
                urgentTypes.push(type);
            }

            const stockItemHTML = `
                <div class="col-md-6 stock-item mb-3">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <span class="fw-bold">${type}</span>
                        <span class="badge ${status.class}">${status.text}</span>
                    </div>
                    <div class="progress" style="height: 8px;">
                        <div class="progress-bar ${status.class}" role="progressbar" style="width: ${percentage}%;" aria-valuenow="${percentage}" aria-valuemin="0" aria-valuemax="100"></div>
                    </div>
                </div>
            `;
            stockLevelsContainer.innerHTML += stockItemHTML;
        });

        // Atualiza a mensagem de alerta
        if (urgentTypes.length > 0) {
            alertMessage.innerHTML = `<i class="fas fa-heart me-1"></i>Sua doação pode salvar vidas! Tipos <strong>${urgentTypes.join(', ')}</strong> são os mais necessários.`;
        } else {
            alertMessage.innerHTML = `<i class="fas fa-check-circle me-1"></i>Obrigado a todos os doadores! Nossos estoques estão estáveis.`;
            alertMessage.classList.replace('alert-danger', 'alert-success');
        }
    }

    window.selectLocation = function(id, name, element) {
        emptyState.style.display = 'none';
        stockPanel.style.display = 'none';
        loadingState.style.display = 'block';

        locationCards.forEach(card => card.classList.remove('selected'));
        element.classList.add('selected');

        setTimeout(() => {
            displayStock(id, name);
            loadingState.style.display = 'none';
            stockPanel.style.display = 'block';
        }, 700);
    };

    searchInput.addEventListener('keyup', function() {
        const filter = searchInput.value.toLowerCase();
        locationCards.forEach(card => {
            const title = card.querySelector('h5').textContent.toLowerCase();
            card.style.display = title.includes(filter) ? '' : 'none';
        });
    });
});
