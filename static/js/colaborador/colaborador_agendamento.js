// JavaScript específico para a página de gestão de agendamentos do colaborador
document.addEventListener('DOMContentLoaded', function() {
    // Função para filtrar agendamentos por horário
    const filtroItems = document.querySelectorAll('.dropdown-item[data-horario]');
    filtroItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const horario = this.getAttribute('data-horario');
            filtrarAgendamentos(horario);
            
            // Atualizar texto do botão
            const botaoFiltro = document.getElementById('horarioFilter');
            botaoFiltro.innerHTML = `<i class="fas fa-clock me-2"></i>${this.textContent}`;
        });
    });

    // Função para filtrar agendamentos por período do dia
    function filtrarAgendamentos(horario) {
        const cards = document.querySelectorAll('.appointment-card');
        let visibleCount = 0;

        cards.forEach(card => {
            if (horario === 'all' || card.getAttribute('data-horario') === horario) {
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

    // Função para cancelar agendamento
    const botoesCancelar = document.querySelectorAll('.btn-cancelar');
    botoesCancelar.forEach(botao => {
        botao.addEventListener('click', function() {
            const agendamentoId = this.getAttribute('data-id');
            mostrarModalCancelarAgendamento(agendamentoId);
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
        
        // Remover o card da lista após confirmação (simulação)
        const card = document.querySelector(`.btn-confirmar[data-id="${agendamentoId}"]`).closest('.appointment-card');
        
        // Animação de fade out
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        card.style.opacity = '0';
        card.style.transform = 'scale(0.9)';
        
        setTimeout(() => {
            card.remove();
            
            // Verificar se ainda há agendamentos
            const totalCards = document.querySelectorAll('.appointment-card').length;
            if (totalCards === 0) {
                document.querySelector('.no-agendamentos-message').style.display = 'block';
            }
        }, 500);
    }

    // Função para mostrar modal de cancelamento
    function mostrarModalCancelarAgendamento(agendamentoId) {
        const modalContent = document.getElementById('modalCancelarContent');
        
        // Buscar informações do card
        const card = document.querySelector(`.btn-cancelar[data-id="${agendamentoId}"]`).closest('.appointment-card');
        const doadorNome = card.querySelector('.doador-name').textContent;
        const dataHora = card.querySelector('.date').textContent.replace('📅', '').trim();
        
        modalContent.innerHTML = `
            <div class="alert alert-warning">
                <i class="fas fa-exclamation-triangle me-2"></i>
                <strong>Atenção!</strong> Esta ação não pode ser desfeita.
            </div>
            <div class="mb-3">
                <p class="mb-2"><strong>Doador:</strong> ${doadorNome}</p>
                <p class="mb-2"><strong>Data/Hora:</strong> ${dataHora}</p>
            </div>
            <div class="mb-3">
                <label for="motivoCancelamento" class="form-label"><strong>Motivo do Cancelamento:</strong></label>
                <textarea class="form-control" id="motivoCancelamento" rows="3" placeholder="Descreva o motivo do cancelamento..."></textarea>
            </div>
            <p class="text-muted mb-0">
                <i class="fas fa-info-circle me-1"></i>
                O doador será notificado sobre o cancelamento.
            </p>
        `;
        
        const modal = new bootstrap.Modal(document.getElementById('cancelarAgendamentoModal'));
        modal.show();
        
        // Configurar ação do botão de confirmação
        const btnConfirmarCancelamento = document.getElementById('btnConfirmarCancelamento');
        btnConfirmarCancelamento.onclick = function() {
            const motivo = document.getElementById('motivoCancelamento').value;
            if (!motivo.trim()) {
                mostrarToast('Por favor, informe o motivo do cancelamento', 'warning');
                return;
            }
            cancelarAgendamento(agendamentoId, motivo);
            modal.hide();
        };
    }

    // Função para cancelar agendamento (simulação)
    function cancelarAgendamento(agendamentoId, motivo) {
        // Em produção, fazer requisição AJAX para cancelar no backend
        console.log('Cancelando agendamento:', agendamentoId, 'Motivo:', motivo);
        
        // Mostrar toast de sucesso
        mostrarToast('Agendamento cancelado com sucesso!', 'success');
        
        // Remover o card da lista após cancelamento
        const card = document.querySelector(`.btn-cancelar[data-id="${agendamentoId}"]`).closest('.appointment-card');
        
        // Animação de fade out
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        card.style.opacity = '0';
        card.style.transform = 'scale(0.9)';
        
        setTimeout(() => {
            card.remove();
            
            // Verificar se ainda há agendamentos
            const totalCards = document.querySelectorAll('.appointment-card').length;
            if (totalCards === 0) {
                document.querySelector('.no-agendamentos-message').style.display = 'block';
            }
        }, 500);
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
        // Re-anexar eventos para botões de detalhes
        document.querySelectorAll('.btn-detalhes').forEach(botao => {
            botao.addEventListener('click', function() {
                const agendamentoId = this.getAttribute('data-id');
                mostrarDetalhesAgendamento(agendamentoId);
            });
        });
        
        // Re-anexar eventos para botões de cancelar
        document.querySelectorAll('.btn-cancelar').forEach(botao => {
            botao.addEventListener('click', function() {
                const agendamentoId = this.getAttribute('data-id');
                mostrarModalCancelarAgendamento(agendamentoId);
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