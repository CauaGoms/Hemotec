// Salve como /static/js/estoque.js

document.addEventListener('DOMContentLoaded', function () {
    const emptyState = document.getElementById('emptyState');
    const loadingState = document.getElementById('loadingState');
    const stockPanel = document.getElementById('stockPanel');
    const stockLevelsGrid = document.getElementById('stock-levels');
    const hemocentroTitle = document.getElementById('stock-hemocentro-title');
    const searchInput = document.getElementById('search-input');
    const locationCards = document.querySelectorAll('.location-card');

    // Dados de estoque simulados para cada hemocentro
    const mockStockData = {
        1: { // Hemocentro Regional
            'A+': { level: 'Estável', percentage: 65 }, 'A-': { level: 'Alerta', percentage: 40 },
            'B+': { level: 'Adequado', percentage: 80 }, 'B-': { level: 'Crítico', percentage: 20 },
            'O+': { level: 'Alerta', percentage: 35 }, 'O-': { level: 'Crítico', percentage: 15 },
            'AB+': { level: 'Adequado', percentage: 90 }, 'AB-': { level: 'Estável', percentage: 55 }
        },
        2: { // Hospital Santa Casa
            'A+': { level: 'Adequado', percentage: 85 }, 'A-': { level: 'Estável', percentage: 60 },
            'B+': { level: 'Estável', percentage: 70 }, 'B-': { level: 'Alerta', percentage: 45 },
            'O+': { level: 'Estável', percentage: 50 }, 'O-': { level: 'Alerta', percentage: 30 },
            'AB+': { level: 'Adequado', percentage: 100 }, 'AB-': { level: 'Estável', percentage: 75 }
        },
        3: { // Unidade Móvel
            'A+': { level: 'Crítico', percentage: 25 }, 'A-': { level: 'Crítico', percentage: 10 },
            'B+': { level: 'Alerta', percentage: 30 }, 'B-': { level: 'Estável', percentage: 50 },
            'O+': { level: 'Alerta', percentage: 40 }, 'O-': { level: 'Estável', percentage: 60 },
            'AB+': { level: 'Estável', percentage: 70 }, 'AB-': { level: 'Adequado', percentage: 80 }
        }
    };

    const levelInfo = {
        'Crítico': { color: 'var(--level-critical)', text: 'Crítico' },
        'Alerta': { color: 'var(--level-alert)', text: 'Alerta' },
        'Estável': { color: 'var(--level-stable)', text: 'Estável' },
        'Adequado': { color: 'var(--level-adequate)', text: 'Adequado' }
    };

    // Função para exibir o estoque
    function displayStock(locationId, locationName) {
        const data = mockStockData[locationId];
        hemocentroTitle.textContent = `Estoque - ${locationName}`;
        stockLevelsGrid.innerHTML = ''; // Limpa o grid anterior

        for (const type in data) {
            const info = data[type];
            const color = levelInfo[info.level].color;
            const levelText = levelInfo[info.level].text;

            const cardHTML = `
                <div class="blood-type-card">
                    <div class="blood-type-label" style="color: ${color};">${type}</div>
                    <div class="progress-bar-container">
                        <div class="progress-bar-fill" style="width: ${info.percentage}%; background-color: ${color};"></div>
                    </div>
                    <div class="level-text" style="color: ${color};">${levelText}</div>
                </div>
            `;
            stockLevelsGrid.innerHTML += cardHTML;
        }
        
        // Atualiza a hora
        document.getElementById('update-time').textContent = new Date().toLocaleString('pt-BR', {
            dateStyle: 'short',
            timeStyle: 'short'
        }).replace(',', ' às');
    }

    // Função chamada ao clicar em um hemocentro
    window.selectLocation = function(id, name, element) {
        // UI states
        emptyState.style.display = 'none';
        stockPanel.style.display = 'none';
        loadingState.style.display = 'flex';

        // Remove a classe 'selected' de todos os cards
        locationCards.forEach(card => card.classList.remove('selected'));
        // Adiciona a classe 'selected' ao card clicado
        element.classList.add('selected');

        // Simula um delay de carregamento (ex: chamada de API)
        setTimeout(() => {
            displayStock(id, name);
            loadingState.style.display = 'none';
            stockPanel.style.display = 'block';
        }, 800); // 0.8 segundos
    };

    // Funcionalidade de busca
    searchInput.addEventListener('keyup', function() {
        const filter = searchInput.value.toLowerCase();
        locationCards.forEach(card => {
            const title = card.querySelector('h5').textContent.toLowerCase();
            if (title.includes(filter)) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    });
});
