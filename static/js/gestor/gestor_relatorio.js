// Relatórios - Página de Seleção

document.addEventListener('DOMContentLoaded', function() {
    // Animação dos cards ao carregar
    const cards = document.querySelectorAll('.report-card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            setTimeout(() => {
                card.style.transition = 'all 0.5s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 50);
        }, index * 100);
    });

    // Adicionar efeito de hover suave aos cards
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
        });
    });

    // Navegação suave ao clicar nos cards
    const cardButtons = document.querySelectorAll('.btn-card');
    cardButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const card = this.closest('.report-card');
            card.style.transform = 'scale(0.95)';
            setTimeout(() => {
                card.style.transform = 'scale(1)';
            }, 150);
        });
    });
});
