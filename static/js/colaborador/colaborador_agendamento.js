// JavaScript específico para a página de gestão de agendamentos do colaborador
document.addEventListener('DOMContentLoaded', function() {
    // Função para filtrar agendamentos por status
    const filtroItems = document.querySelectorAll('.dropdown-item[data-status]');
    filtroItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const status = this.getAttribute('data-status');
            filtrarAgendamentos(status);
            
            // Atualizar texto do botão
            const botaoFiltro = document.getElementById('statusFilter');
            botaoFiltro.innerHTML = `<i class="fas fa-filter me-2"></i>${this.textContent}`;
        });
    });

    // Função para filtrar agendamentos
    function filtrarAgendamentos(status) {
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

        // Mostrar/ocultar mensagem de "nenhum agendamento"
        const mensagemVazia = document.querySelector('.no-agendamentos-message');
        if (visibleCount === 0) {
            mensagemVazia.style.display = 'block';
        } else {
            mensagemVazia.style.display = 'none';
        }
    }

    // Função para confirmar presença
    const botoesConfirmar = document.querySelectorAll('.btn-confirmar');
    botoesConfirmar.forEach(botao => {
        botao.addEventListener('click', function() {
            const agendamentoId = this.getAttribute('data-id');
            mostrarModalConfirmarPresenca(agendamentoId);
        });
    });

    // Função para mostrar modal de confirmação de presença
    function mostrarModalConfirmarPresenca(agendamentoId) {
        const modalContent = document.getElementById('modalConfirmarContent');
        
        // Simulação de dados do agendamento (em produção, buscar via AJAX)
        const agendamento = {
            id: agendamentoId,
            doador: 'Maria Santos Silva',
            data: '15/10/2025 09:00',
            tipo: 'A+',
            local: 'Hemocentro Regional'
        };
        
        modalContent.innerHTML = `
            <div class="text-center mb-3">
                <i class="fas fa-user-check fa-3x text-success mb-3"></i>
                <h5>Confirmar presença do doador?</h5>
            </div>
            <div class="alert alert-info">
                <strong>Doador:</strong> ${agendamento.doador}<br>
                <strong>Data/Hora:</strong> ${agendamento.data}<br>
                <strong>Tipo Sanguíneo:</strong> ${agendamento.tipo}<br>
                <strong>Local:</strong> ${agendamento.local}
            </div>
            <p class="text-muted mb-0">
                <i class="fas fa-info-circle me-1"></i>
                Ao confirmar, o status do agendamento será atualizado e o doador poderá iniciar o processo de doação.
            </p>
        `;
        
        const modal = new bootstrap.Modal(document.getElementById('confirmarPresencaModal'));
        modal.show();
        
        // Configurar ação do botão de confirmação
        const btnConfirmar = document.getElementById('btnConfirmarPresenca');
        btnConfirmar.onclick = function() {
            confirmarPresenca(agendamentoId);
            modal.hide();
        };
    }

    // Função para confirmar presença (simulação)
    function confirmarPresenca(agendamentoId) {
        // Em produção, fazer requisição AJAX para confirmar no backend
        console.log('Confirmando presença do agendamento:', agendamentoId);
        
        // Mostrar toast de sucesso
        mostrarToast('Presença confirmada com sucesso!', 'success');
        
        // Atualizar visualmente o card (simulação)
        const card = document.querySelector(`.btn-confirmar[data-id="${agendamentoId}"]`).closest('.appointment-card');
        
        // Alterar badge
        const badge = card.querySelector('.status-badge');
        badge.className = 'status-badge confirmado-badge';
        badge.innerHTML = '<i class="fas fa-check-circle me-1"></i> Presença Confirmada';
        
        // Alterar borda
        card.className = 'appointment-card confirmado';
        card.setAttribute('data-status', 'confirmado');
        
        // Alterar botões de ação
        const actions = card.querySelector('.actions');
        actions.innerHTML = `
            <button class="btn btn-iniciar-doacao" data-id="${agendamentoId}">
                <i class="fas fa-play me-1"></i> Iniciar Doação
            </button>
            <button class="btn btn-detalhes" data-id="${agendamentoId}">
                <i class="fas fa-eye me-1"></i> Ver Detalhes
            </button>
        `;
        
        // Re-anexar eventos aos novos botões
        anexarEventos();
    }

    // Função para iniciar doação
    function iniciarDoacao(agendamentoId) {
        // Em produção, redirecionar para página de doação ou iniciar fluxo
        console.log('Iniciando doação do agendamento:', agendamentoId);
        mostrarToast('Redirecionando para o processo de doação...', 'info');
        
        // Simulação: redirecionar após 1 segundo
        setTimeout(() => {
            window.location.href = `/colaborador/doacoes/adicionar?agendamento_id=${agendamentoId}`;
        }, 1000);
    }

    // Função para ver doação
    function verDoacao(agendamentoId) {
        // Em produção, redirecionar para detalhes da doação
        console.log('Visualizando doação do agendamento:', agendamentoId);
        window.location.href = `/colaborador/doacoes/detalhes/${agendamentoId}`;
    }

    // Função para ver detalhes
    const botoesDetalhes = document.querySelectorAll('.btn-detalhes');
    botoesDetalhes.forEach(botao => {
        botao.addEventListener('click', function() {
            const agendamentoId = this.getAttribute('data-id');
            mostrarDetalhesAgendamento(agendamentoId);
        });
    });

    // Função para mostrar detalhes do agendamento
    function mostrarDetalhesAgendamento(agendamentoId) {
        const modalContent = document.getElementById('modalDetailsContent');
        
        // Simulação de dados detalhados (em produção, buscar via AJAX)
        const detalhes = {
            id: agendamentoId,
            doador: 'Maria Santos Silva',
            cpf: '123.456.789-00',
            data_nascimento: '15/03/1985',
            idade: '40 anos',
            tipo_sanguineo: 'A+',
            telefone: '(28) 99999-8888',
            email: 'maria.santos@email.com',
            data_agendamento: '15/10/2025 09:00',
            local: 'Hemocentro Regional',
            endereco: 'Rua Principal, 100 - Centro',
            status: 'Pendente',
            observacoes: 'Primeira doação do doador',
            ultima_doacao: 'Nunca doou',
            apto_doar: 'Sim'
        };
        
        modalContent.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <h6 class="text-primary mb-3"><i class="fas fa-user me-2"></i>Dados do Doador</h6>
                    <ul class="list-unstyled mb-3">
                        <li class="mb-2"><strong>Nome:</strong> ${detalhes.doador}</li>
                        <li class="mb-2"><strong>CPF:</strong> ${detalhes.cpf}</li>
                        <li class="mb-2"><strong>Data Nascimento:</strong> ${detalhes.data_nascimento} (${detalhes.idade})</li>
                        <li class="mb-2"><strong>Tipo Sanguíneo:</strong> <span class="badge bg-danger">${detalhes.tipo_sanguineo}</span></li>
                        <li class="mb-2"><strong>Telefone:</strong> ${detalhes.telefone}</li>
                        <li class="mb-2"><strong>E-mail:</strong> ${detalhes.email}</li>
                    </ul>
                </div>
                <div class="col-md-6">
                    <h6 class="text-success mb-3"><i class="fas fa-calendar-check me-2"></i>Dados do Agendamento</h6>
                    <ul class="list-unstyled mb-3">
                        <li class="mb-2"><strong>Data/Hora:</strong> ${detalhes.data_agendamento}</li>
                        <li class="mb-2"><strong>Local:</strong> ${detalhes.local}</li>
                        <li class="mb-2"><strong>Endereço:</strong> ${detalhes.endereco}</li>
                        <li class="mb-2"><strong>Status:</strong> <span class="badge bg-warning">${detalhes.status}</span></li>
                        <li class="mb-2"><strong>ID:</strong> ${detalhes.id}</li>
                    </ul>
                </div>
            </div>
            <hr>
            <div class="row">
                <div class="col-md-12">
                    <h6 class="text-info mb-3"><i class="fas fa-notes-medical me-2"></i>Informações Adicionais</h6>
                    <ul class="list-unstyled mb-3">
                        <li class="mb-2"><strong>Última Doação:</strong> ${detalhes.ultima_doacao}</li>
                        <li class="mb-2"><strong>Apto para Doar:</strong> 
                            <span class="badge bg-success">${detalhes.apto_doar}</span>
                        </li>
                        <li class="mb-2"><strong>Observações:</strong> ${detalhes.observacoes}</li>
                    </ul>
                </div>
            </div>
        `;
        
        const modal = new bootstrap.Modal(document.getElementById('detailsModal'));
        modal.show();
    }

    // Função para anexar eventos dinamicamente
    function anexarEventos() {
        // Re-anexar eventos para botões de iniciar doação
        document.querySelectorAll('.btn-iniciar-doacao').forEach(botao => {
            botao.addEventListener('click', function() {
                const agendamentoId = this.getAttribute('data-id');
                iniciarDoacao(agendamentoId);
            });
        });

        // Re-anexar eventos para botões de ver doação
        document.querySelectorAll('.btn-ver-doacao').forEach(botao => {
            botao.addEventListener('click', function() {
                const agendamentoId = this.getAttribute('data-id');
                verDoacao(agendamentoId);
            });
        });

        // Re-anexar eventos para botões de detalhes
        document.querySelectorAll('.btn-detalhes').forEach(botao => {
            botao.addEventListener('click', function() {
                const agendamentoId = this.getAttribute('data-id');
                mostrarDetalhesAgendamento(agendamentoId);
            });
        });
    }

    // Função para mostrar toast de notificação
    function mostrarToast(mensagem, tipo = 'info') {
        // Criar elemento de toast
        const toastContainer = document.createElement('div');
        toastContainer.className = 'position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        
        const iconMap = {
            'success': 'check-circle',
            'error': 'times-circle',
            'warning': 'exclamation-triangle',
            'info': 'info-circle'
        };
        
        const bgMap = {
            'success': 'success',
            'error': 'danger',
            'warning': 'warning',
            'info': 'info'
        };
        
        toastContainer.innerHTML = `
            <div class="toast align-items-center text-white bg-${bgMap[tipo]} border-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        <i class="fas fa-${iconMap[tipo]} me-2"></i>
                        ${mensagem}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `;
        
        document.body.appendChild(toastContainer);
        const toastElement = toastContainer.querySelector('.toast');
        const toast = new bootstrap.Toast(toastElement, { delay: 3000 });
        toast.show();
        
        // Remover após fechar
        toastElement.addEventListener('hidden.bs.toast', function() {
            toastContainer.remove();
        });
    }

    // Anexar eventos iniciais
    anexarEventos();

    // Verificar inicialmente se há agendamentos
    const totalCards = document.querySelectorAll('.appointment-card').length;
    if (totalCards === 0) {
        document.querySelector('.no-agendamentos-message').style.display = 'block';
    }
});