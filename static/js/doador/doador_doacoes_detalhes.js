/**
 * ======================================
 * JavaScript para Página de Detalhes da Doação
 * ====================================== 
 */

// Configurar eventos de impressão
window.onbeforeprint = function() {
    document.body.classList.add('printing');
    console.log('Preparando para impressão...');
};

window.onafterprint = function() {
    document.body.classList.remove('printing');
    console.log('Impressão finalizada.');
};

// Função para baixar PDF (placeholder)
function baixarPDF(codDoacao) {
    // Fazer download do PDF gerado pelo backend
    window.location.href = `/doador/doacoes/comprovante/pdf/${codDoacao}`;
}

// Função para imprimir comprovante
function imprimirComprovante() {
    window.print();
}

// Adicionar listeners quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    console.log('Página de detalhes da doação carregada');
    
    // Verificar se há botão de download PDF e adicionar funcionalidade
    const btnDownloadPDF = document.querySelector('button[onclick*="download"]');
    if (btnDownloadPDF) {
        btnDownloadPDF.onclick = baixarPDF;
    }
    
    // Verificar se há botão de impressão e adicionar funcionalidade
    const btnPrint = document.querySelector('button[onclick*="print"]');
    if (btnPrint) {
        btnPrint.onclick = imprimirComprovante;
    }
    
    // Animação suave ao carregar cards
    const detailCards = document.querySelectorAll('.detail-card');
    detailCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 * index);
    });
});

// Função para voltar à página anterior
function voltarHistorico() {
    window.location.href = '/doador/doacoes';
}
