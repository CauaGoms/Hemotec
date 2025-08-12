// Salve como /static/js/carteira_doador_horizontal.js
document.addEventListener('DOMContentLoaded', function () {
    // Seleciona o botão de download e o elemento da carteirinha
    const downloadButton = document.getElementById('download-btn');
    const donorCardElement = document.getElementById('donor-card');

    // Verifica se os elementos existem na página antes de adicionar o evento
    if (downloadButton && donorCardElement) {
        downloadButton.addEventListener('click', function () {
            // Desabilita o botão e mostra um feedback de carregamento
            downloadButton.disabled = true;
            downloadButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Gerando PDF...';

            const cardWidth = 600; // mesmo valor do CSS
            const cardHeight = 350; // mesmo valor do CSS
            // Define as opções para a geração do PDF
            const opt = {
                margin:       0,
                filename:     'carteira-doador-hemotec.pdf',
                image:        { type: 'jpeg', quality: 1.0 },
                html2canvas:  { scale: 2, logging: true, useCORS: true }, // Aumenta a escala para máxima qualidade
                jsPDF: { unit: 'px', format: [cardWidth, cardHeight] }
            };

            // Usa a biblioteca html2pdf para criar e baixar o PDF
            html2pdf().from(donorCardElement).set(opt).save().then(() => {
                // Após o download (ou falha), restaura o botão
                downloadButton.disabled = false;
                downloadButton.innerHTML = '<i class="fas fa-download me-2"></i>Baixar Carteirinha (PDF)';
            }).catch((error) => {
                console.error("Erro ao gerar o PDF:", error);
                // Restaura o botão mesmo em caso de erro
                downloadButton.disabled = false;
                downloadButton.innerHTML = '<i class="fas fa-exclamation-circle me-2"></i>Tente Novamente';
            });
        });
    }
});
