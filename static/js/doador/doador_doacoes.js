// JavaScript específico para a página de histórico de doações
document.addEventListener('DOMContentLoaded', function() {
    // Função para filtrar doações por status
    const filtroItems = document.querySelectorAll('[data-status]');
    filtroItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const status = this.getAttribute('data-status');
            filtrarDoacoes(status);
            
            // Atualizar texto do botão
            const botaoFiltro = document.getElementById('statusFilter');
            botaoFiltro.innerHTML = `<i class="fas fa-filter me-2"></i>${this.textContent}`;
        });
    });

    // Função para filtrar doações
    function filtrarDoacoes(status) {
        const cards = document.querySelectorAll('.appointment-card');
        let visibleCount = 0;

        cards.forEach(card => {
            if (status === 'all' || card.getAttribute('data-status') === status) {
                card.style.display = 'block';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Mostrar/ocultar mensagem de "nenhuma doação"
        const mensagemVazia = document.querySelector('.no-donations-message');
        if (visibleCount === 0) {
            mensagemVazia.style.display = 'block';
        } else {
            mensagemVazia.style.display = 'none';
        }
    }

    // Função para ver comprovante
    const botoesComprovante = document.querySelectorAll('.btn-comprovante');
    botoesComprovante.forEach(botao => {
        botao.addEventListener('click', function() {
            const doacaoId = this.getAttribute('data-id');
            mostrarComprovanteDoacao(doacaoId);
        });
    });

        // Função para mostrar comprovante da doação em modal
        function mostrarComprovanteDoacao(doacaoId) {
            const modalContent = document.getElementById('modalDetailsContent');
            // Simulação de dados detalhados (em produção, buscar via AJAX)
            const detalhes = {
                nome: 'João da Silva',
                data: '15/04/2025 09:00',
                local: 'Hospital Santa Casa',
                endereco: 'Av. Beira Rio, 1200 - Independência',
                tipo: 'O+',
                status: 'Concluída',
                id: doacaoId
            };
            modalContent.innerHTML = `
                <div class="row">
                    <div class="col-md-7">
                        <h5 class="mb-2">Comprovante de Doação</h5>
                        <ul class="list-unstyled mb-3">
                            <li><strong>Nome do Doador:</strong> ${detalhes.nome}</li>
                            <li><strong>Data e Hora:</strong> ${detalhes.data}</li>
                            <li><strong>Local:</strong> ${detalhes.local}</li>
                            <li><strong>Endereço:</strong> ${detalhes.endereco}</li>
                            <li><strong>Tipo Sanguíneo:</strong> ${detalhes.tipo}</li>
                            <li><strong>Status:</strong> <span class="text-success">${detalhes.status}</span></li>
                            <li><strong>ID da Doação:</strong> ${detalhes.id}</li>
                        </ul>
                        <div class="alert alert-success p-2 mb-2">
                            <i class="fas fa-check-circle me-2"></i>
                            Doação registrada e validada pelo sistema Hemotec.
                        </div>
                        <p class="text-muted mb-0">Este comprovante é válido em todo o território nacional.</p>
                    </div>
                    <div class="col-md-5 text-center">
                        <img src="/doador/comprovante/${doacaoId}" alt="Comprovante" style="max-width: 100%; max-height: 250px; border-radius: 10px; box-shadow: 0 2px 12px rgba(0,0,0,0.08);">
                        <div class="mt-2">
                            <button class="btn btn-outline-primary btn-sm" onclick="window.print()"><i class="fas fa-print me-1"></i> Imprimir</button>
                        </div>
                    </div>
                </div>
            `;
            const modal = new bootstrap.Modal(document.getElementById('detailsModal'));
            modal.show();
        }

    // Função para acompanhar status
    const botoesStatus = document.querySelectorAll('.btn-status');
    botoesStatus.forEach(botao => {
        botao.addEventListener('click', function() {
            const doacaoId = this.getAttribute('data-id');
            mostrarDetalhesStatus(doacaoId);
        });
    });

    // Função para ver detalhes
    const botoesDetalhes = document.querySelectorAll('.btn-detalhes');
    botoesDetalhes.forEach(botao => {
        botao.addEventListener('click', function() {
            const doacaoId = this.getAttribute('data-id');
            mostrarDetalhesDoacao(doacaoId);
        });
    });

    // Função para mostrar detalhes do status
    function mostrarDetalhesStatus(doacaoId) {
        const modalContent = document.getElementById('modalDetailsContent');
        modalContent.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <h6>Status Atual</h6>
                    <p class="text-info"><i class="fas fa-hourglass-half me-2"></i>Aguardando Exame</p>
                </div>
                <div class="col-md-6">
                    <h6>Previsão de Resultado</h6>
                    <p>3-5 dias úteis</p>
                </div>
            </div>
            <hr>
            <h6>Histórico de Status</h6>
            <ul class="list-unstyled">
                <li class="mb-2">
                    <i class="fas fa-check text-success me-2"></i>
                    <strong>20/05/2025 08:30</strong> - Doação realizada com sucesso
                </li>
                <li class="mb-2">
                    <i class="fas fa-vial text-primary me-2"></i>
                    <strong>20/05/2025 09:15</strong> - Amostra enviada para laboratório
                </li>
                <li class="mb-2">
                    <i class="fas fa-hourglass-half text-warning me-2"></i>
                    <strong>20/05/2025 10:00</strong> - Aguardando resultados dos exames
                </li>
            </ul>
        `;
        
        const modal = new bootstrap.Modal(document.getElementById('detailsModal'));
        modal.show();
    }

    // Função para mostrar detalhes da doação
    function mostrarDetalhesDoacao(doacaoId) {
        const modalContent = document.getElementById('modalDetailsContent');
        modalContent.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <h6>Status</h6>
                    <p class="text-warning"><i class="fas fa-exclamation-triangle me-2"></i>Recusada</p>
                </div>
                <div class="col-md-6">
                    <h6>Data da Tentativa</h6>
                    <p>08/03/2025 15:45</p>
                </div>
            </div>
            <hr>
            <h6>Motivo da Recusa</h6>
            <p>Hemoglobina baixa detectada no teste inicial (10.2 g/dL). O valor mínimo necessário é 12.5 g/dL para mulheres e 13.0 g/dL para homens.</p>
            
            <h6>Recomendações</h6>
            <ul>
                <li>Consulte um médico para avaliação da anemia</li>
                <li>Aumente o consumo de alimentos ricos em ferro</li>
                <li>Aguarde pelo menos 8 semanas antes de tentar doar novamente</li>
                <li>Realize exames de sangue para acompanhamento</li>
            </ul>
            
            <div class="alert alert-info">
                <i class="fas fa-info-circle me-2"></i>
                Você pode tentar doar novamente após seguir as recomendações médicas e aguardar o período mínimo.
            </div>
        `;
        
        const modal = new bootstrap.Modal(document.getElementById('detailsModal'));
        modal.show();
    }

    // Verificar inicialmente se há doações
    const totalCards = document.querySelectorAll('.appointment-card').length;
    if (totalCards === 0) {
        document.querySelector('.no-donations-message').style.display = 'block';
    }
});