// Relatórios por Período

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('filterForm');
    const btnExport = document.querySelector('.btnExportPDF');

    // Definir data padrão (últimos 30 dias)
    const hoje = new Date();
    const dataFim = document.getElementById('data_fim');
    const dataInicio = document.getElementById('data_inicio');
    
    if (dataFim && !dataFim.value) {
        dataFim.value = hoje.toISOString().split('T')[0];
    }
    
    if (dataInicio && !dataInicio.value) {
        const trintaDiasAtras = new Date();
        trintaDiasAtras.setDate(hoje.getDate() - 30);
        dataInicio.value = trintaDiasAtras.toISOString().split('T')[0];
    }

    // Validar datas ao submeter formulário
    if (form) {
        form.addEventListener('submit', function(e) {
            const inicio = new Date(dataInicio.value);
            const fim = new Date(dataFim.value);
            
            if (inicio > fim) {
                e.preventDefault();
                alert('A data inicial não pode ser posterior à data final.');
                return false;
            }
            
            if (fim > hoje) {
                e.preventDefault();
                alert('A data final não pode ser posterior à data atual.');
                return false;
            }
        });
    }

    // Exportar PDF
    if (btnExport) {
        btnExport.addEventListener('click', function(e) {
            e.preventDefault();
            
            const dataInicioValue = dataInicio.value;
            const dataFimValue = dataFim.value;
            
            if (!dataInicioValue || !dataFimValue) {
                alert('Por favor, selecione ambas as datas antes de exportar.');
                return;
            }
            
            const inicio = new Date(dataInicioValue);
            const fim = new Date(dataFimValue);
            
            if (inicio > fim) {
                alert('A data inicial não pode ser posterior à data final.');
                return;
            }
            
            // Construir URL com parâmetros
            const params = new URLSearchParams();
            if (dataInicioValue) params.append('data_inicio', dataInicioValue);
            if (dataFimValue) params.append('data_fim', dataFimValue);
            
            // Feedback visual
            btnExport.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Gerando PDF...';
            btnExport.disabled = true;
            
            // Redirecionar para rota de PDF
            const pdfUrl = `/administrador/relatorios/periodo/pdf?${params.toString()}`;
            window.location.href = pdfUrl;
            
            // Restaurar botão após um tempo
            setTimeout(() => {
                btnExport.innerHTML = '<i class="fas fa-file-pdf"></i> Exportar PDF';
                btnExport.disabled = false;
            }, 2000);
        });
    }

    // Animação dos cards de estatísticas
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach((card, index) => {
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

    // Animação dos valores das estatísticas
    const statValues = document.querySelectorAll('.stat-value');
    statValues.forEach(stat => {
        const finalValue = parseInt(stat.textContent);
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
});
