document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.plano-card button');
    
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const planoCard = this.closest('.plano-card');
            const planoTitulo = planoCard.querySelector('h2').textContent;
            const planoPreco = planoCard.querySelector('.preco').textContent;
            
            if (this.textContent === 'Entre em Contato') {
                alert('Para planos personalizados, entre em contato conosco através do email: contato@hemotec.com.br');
            } else {
                const confirmacao = confirm(`Você deseja selecionar o ${planoTitulo} por ${planoPreco}?`);
                if (confirmacao) {
                    // Aqui você pode redirecionar para a página de pagamento ou processar a seleção
                    alert('Plano selecionado! Redirecionando para finalização...');
                    // window.location.href = 'publico_finalizar_cadastro.html';
                }
            }
        });
        
        // Adiciona efeito hover
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
            this.style.transition = 'transform 0.2s ease';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    // Adiciona animação aos cards quando a página carrega
    const planoCards = document.querySelectorAll('.plano-card');
    planoCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});

