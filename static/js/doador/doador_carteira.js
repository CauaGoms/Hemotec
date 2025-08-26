// Salve como /static/js/carteira_doador_horizontal.js
document.addEventListener('DOMContentLoaded', function () {
    // Seleciona o botão de download e o elemento da carteirinha
    const downloadButton = document.getElementById('download-btn');
    const donorCardElement = document.getElementById('donor-card');

    // Função para mostrar alerta ao usuário
    function showAlert(message) {
        alert(message);
    }

    // Verifica se os elementos existem na página antes de adicionar o evento
    if (downloadButton && donorCardElement) {
        downloadButton.addEventListener('click', function () {
            // Desabilita o botão e mostra um feedback de carregamento
            downloadButton.disabled = true;
            downloadButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Gerando PDF...';

            // Configuração para gerar PDF em folha A4 horizontal (landscape)
            const opt = {
                margin: 10,
                filename: 'carteira-doador-hemotec.pdf',
                image: { type: 'jpeg', quality: 1.0 },
                html2canvas: { scale: 2, logging: true, useCORS: true },
                jsPDF: { unit: 'mm', format: [297, 210], orientation: 'landscape' }
            };

            // Usa a biblioteca html2pdf para criar e baixar o PDF
            html2pdf().from(donorCardElement).set(opt).save().then(() => {
                // Após o download, restaura o botão
                downloadButton.disabled = false;
                downloadButton.innerHTML = '<i class="fas fa-download me-2"></i>Baixar Carteirinha (PDF)';
            }).catch((error) => {
                console.error("Erro ao gerar o PDF:", error);
                showAlert("Erro ao gerar o PDF. Verifique sua conexão ou tente novamente. Se o problema persistir, entre em contato com o suporte.");
                downloadButton.disabled = false;
                downloadButton.innerHTML = '<i class="fas fa-exclamation-circle me-2"></i>Tente Novamente';
            });
        });
    } else {
        // Se os elementos não existirem, mostra alerta
        showAlert("Não foi possível encontrar a carteirinha ou o botão de download na página.");
    }
});
