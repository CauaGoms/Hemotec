// Relatórios por Tipo Sanguíneo

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('filterForm');
    const btnExport = document.querySelector('.btnExportPDF');
    const selectTipo = document.getElementById('tipo_sanguineo');

    // Exportar PDF
    if (btnExport) {
        btnExport.addEventListener('click', function(e) {
            e.preventDefault();
            
            const tipoSanguineo = selectTipo.value;
            
            // Construir URL com parâmetros
            const params = new URLSearchParams();
            if (tipoSanguineo && tipoSanguineo !== 'todos') {
                params.append('tipo_sanguineo', tipoSanguineo);
            }
            
            // Feedback visual
            btnExport.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Gerando PDF...';
            btnExport.disabled = true;
            
            // Redirecionar para rota de PDF
            const pdfUrl = `/administrador/relatorios/tipo_sanguineo/pdf?${params.toString()}`;
            window.location.href = pdfUrl;
            
            // Restaurar botão após um tempo
            setTimeout(() => {
                btnExport.innerHTML = '<i class="fas fa-file-pdf"></i> Exportar PDF';
                btnExport.disabled = false;
            }, 2000);
        });
    }

    // Animação dos cards de tipo sanguíneo
    const bloodCards = document.querySelectorAll('.blood-type-card');
    bloodCards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            setTimeout(() => {
                card.style.transition = 'all 0.5s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 50);
        }, index * 80);
    });

    // Animação dos valores das estatísticas
    const bloodStatValues = document.querySelectorAll('.blood-stat-value');
    bloodStatValues.forEach(stat => {
        const finalValue = parseInt(stat.textContent);
        if (isNaN(finalValue)) return;
        
        let currentValue = 0;
        const increment = Math.ceil(finalValue / 30);
        
        const counter = setInterval(() => {
            currentValue += increment;
            if (currentValue >= finalValue) {
                stat.textContent = finalValue;
                clearInterval(counter);
            } else {
                stat.textContent = currentValue;
            }
        }, 30);
    });

    // Destacar tipo sanguíneo selecionado
    if (selectTipo) {
        selectTipo.addEventListener('change', function() {
            const selectedType = this.value;
            
            // Remover destaque de todos os cards
            bloodCards.forEach(card => {
                card.style.opacity = '0.5';
                card.style.transform = 'scale(0.95)';
            });
            
            // Se não for "todos", destacar o selecionado
            if (selectedType !== 'todos') {
                const selectedCard = document.querySelector(`[data-type="${selectedType}"]`);
                if (selectedCard) {
                    selectedCard.style.opacity = '1';
                    selectedCard.style.transform = 'scale(1.05)';
                    selectedCard.style.boxShadow = '0 12px 40px rgba(220, 20, 60, 0.25)';
                    
                    // Scroll suave até o card
                    setTimeout(() => {
                        selectedCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }, 100);
                }
            } else {
                // Restaurar todos os cards
                bloodCards.forEach(card => {
                    card.style.opacity = '1';
                    card.style.transform = 'scale(1)';
                    card.style.boxShadow = '';
                });
            }
        });
    }

    // Adicionar data-type aos cards baseado no texto do tipo sanguíneo
    bloodCards.forEach(card => {
        const typeElement = card.querySelector('.blood-type');
        if (typeElement) {
            const bloodType = typeElement.textContent.trim();
            card.setAttribute('data-type', bloodType);
        }
    });

    // Colorir badges de status na tabela de estoque
    const statusBadges = document.querySelectorAll('td .badge');
    statusBadges.forEach(badge => {
        const text = badge.textContent.trim().toLowerCase();
        if (text === 'suficiente') {
            badge.classList.add('badge-success');
        } else if (text === 'atenção') {
            badge.classList.add('badge-warning');
        } else if (text === 'crítico') {
            badge.classList.add('badge-danger');
        }
    });
});
