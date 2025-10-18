// Gestão de Doações - Colaborador - JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const filterButtons = document.querySelectorAll('.filter-btn');
    const donationCards = document.querySelectorAll('.donation-card');
    const searchInput = document.getElementById('searchInput');
    const noDoacoesMessage = document.getElementById('noDoacoesMessage');

    // Filtrar por status
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const status = this.dataset.status;
            
            // Atualizar botão ativo
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            // Filtrar cards
            let visibleCount = 0;
            donationCards.forEach(card => {
                if (status === 'all' || card.dataset.status === status) {
                    card.style.display = '';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            // Mostrar mensagem se não há resultados
            if (visibleCount === 0) {
                noDoacoesMessage.style.display = 'block';
            } else {
                noDoacoesMessage.style.display = 'none';
            }
        });
    });

    // Buscar por nome, CPF ou telefone
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            let visibleCount = 0;

            donationCards.forEach(card => {
                const cardText = card.textContent.toLowerCase();

                if (searchTerm === '' || cardText.includes(searchTerm)) {
                    card.style.display = '';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            // Mostrar mensagem se não há resultados
            if (visibleCount === 0 && searchTerm !== '') {
                noDoacoesMessage.style.display = 'block';
            } else {
                noDoacoesMessage.style.display = 'none';
            }
        });
    }
});

