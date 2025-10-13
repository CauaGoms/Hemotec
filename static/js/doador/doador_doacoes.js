// JavaScript específico para a página de histórico de doações
document.addEventListener('DOMContentLoaded', function() {
    // Função para filtrar doações por status
    const filtroItems = document.querySelectorAll('.dropdown-item[data-status]');
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
        
        // Mostrar loading
        modalContent.innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Carregando...</span>
                </div>
                <p class="mt-3">Carregando detalhes...</p>
            </div>
        `;
        
        const modal = new bootstrap.Modal(document.getElementById('detailsModal'));
        modal.show();
        
        // Buscar dados da API
        fetch(`/api/doador/doacao/${doacaoId}/detalhes`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao buscar detalhes');
                }
                return response.json();
            })
            .then(data => {
                // Montar HTML com dados reais
                let html = `
                    <div class="row">
                        <div class="col-md-6">
                            <h6>Status</h6>
                            <p class="text-warning"><i class="fas fa-exclamation-triangle me-2"></i>${getStatusText(data.doacao.status)}</p>
                        </div>
                        <div class="col-md-6">
                            <h6>Data da Tentativa</h6>
                            <p>${formatarDataHora(data.doacao.data_hora)}</p>
                        </div>
                    </div>
                    <hr>
                    
                    <h6>Local da Doação</h6>
                    <p><i class="fas fa-hospital me-2"></i>${data.unidade.nome || 'Não especificada'}</p>
                    <p class="text-muted">${data.unidade.endereco_completo || 'Endereço não disponível'}</p>
                `;
                
                // Adicionar observações se existirem
                if (data.doacao.observacoes) {
                    html += `
                        <hr>
                        <h6>Motivo da Recusa</h6>
                        <p>${data.doacao.observacoes}</p>
                    `;
                }
                
                // Adicionar informações do prontuário se existir
                if (data.prontuario) {
                    html += `
                        <hr>
                        <h6>Informações da Triagem</h6>
                        <ul class="list-unstyled">
                    `;
                    
                    if (data.prontuario.diabetes) html += '<li><i class="fas fa-times text-danger me-2"></i>Diabetes detectado</li>';
                    if (data.prontuario.hipertensao) html += '<li><i class="fas fa-times text-danger me-2"></i>Hipertensão detectada</li>';
                    if (data.prontuario.cardiopatia) html += '<li><i class="fas fa-times text-danger me-2"></i>Cardiopatia detectada</li>';
                    if (data.prontuario.cancer) html += '<li><i class="fas fa-times text-danger me-2"></i>Histórico de câncer</li>';
                    if (data.prontuario.hepatite) html += '<li><i class="fas fa-times text-danger me-2"></i>Hepatite detectada</li>';
                    if (data.prontuario.sintomas_gripais) html += '<li><i class="fas fa-times text-danger me-2"></i>Sintomas gripais</li>';
                    if (data.prontuario.alcool) html += '<li><i class="fas fa-times text-danger me-2"></i>Consumo de álcool recente</li>';
                    
                    if (data.prontuario.medicamentos && data.prontuario.detalhes_medicamentos) {
                        html += `<li><i class="fas fa-pills text-warning me-2"></i>Medicamentos: ${data.prontuario.detalhes_medicamentos}</li>`;
                    }
                    
                    html += '</ul>';
                }
                
                // Adicionar exames se existirem
                if (data.exames && data.exames.length > 0) {
                    html += `
                        <hr>
                        <h6>Exames Realizados</h6>
                        <ul class="list-unstyled">
                    `;
                    
                    data.exames.forEach(exame => {
                        const resultadoClass = exame.resultado.toLowerCase().includes('negativo') || exame.resultado.toLowerCase().includes('normal') ? 'text-success' : 'text-danger';
                        html += `
                            <li class="mb-2">
                                <strong>${exame.tipo_exame}</strong><br>
                                <span class="${resultadoClass}">Resultado: ${exame.resultado}</span><br>
                                <small class="text-muted">Data: ${formatarData(exame.data_exame)}</small>
                            </li>
                        `;
                    });
                    
                    html += '</ul>';
                }
                
                // Adicionar recomendações se for status recusado
                if (data.doacao.status === 1) {
                    html += `
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle me-2"></i>
                            Você pode tentar doar novamente após seguir as recomendações médicas e aguardar o período mínimo.
                        </div>
                    `;
                }
                
                modalContent.innerHTML = html;
            })
            .catch(error => {
                console.error('Erro:', error);
                modalContent.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-circle me-2"></i>
                        Erro ao carregar os detalhes. Por favor, tente novamente.
                    </div>
                `;
            });
    }
    
    // Funções auxiliares para formatação
    function getStatusText(status) {
        const statusMap = {
            0: 'Cancelada',
            1: 'Recusada',
            2: 'Aguardando Exame',
            3: 'Concluída'
        };
        return statusMap[status] || 'Desconhecido';
    }
    
    function formatarDataHora(dataHora) {
        if (!dataHora) return 'Data não disponível';
        const data = new Date(dataHora);
        return data.toLocaleString('pt-BR', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
    
    function formatarData(data) {
        if (!data) return 'Data não disponível';
        const d = new Date(data);
        return d.toLocaleDateString('pt-BR', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        });
    }

    // Verificar inicialmente se há doações
    const totalCards = document.querySelectorAll('.appointment-card').length;
    if (totalCards === 0) {
        document.querySelector('.no-donations-message').style.display = 'block';
    }
});