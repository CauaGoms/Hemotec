// Variáveis globais
let currentFilter = 'all';
let notifications = [];

// Inicializar página
document.addEventListener('DOMContentLoaded', function () {
    loadNotifications();
    updateStats();

    // Animações de entrada
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    });

    document.querySelectorAll('.fade-in').forEach(el => {
        observer.observe(el);
    });
});

// Carregar notificações
function loadNotifications() {
    // Simular carregamento de dados
    notifications = Array.from(document.querySelectorAll('.notification-item'));
    updateNotificationDisplay();
}

// Filtrar notificações
function filterNotifications(filter) {
    currentFilter = filter;

    // Atualizar botões de filtro
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-filter="${filter}"]`).classList.add('active');

    updateNotificationDisplay();
}

// Atualizar exibição das notificações
function updateNotificationDisplay() {
    notifications.forEach(notification => {
        const type = notification.getAttribute('data-type');
        const isUnread = notification.classList.contains('unread');
        const isImportant = notification.classList.contains('critical') || notification.classList.contains('result');
        const isCampaign = notification.classList.contains('campaign');

        let shouldShow = false;

        switch (currentFilter) {
            case 'all':
                shouldShow = true;
                break;
            case 'unread':
                shouldShow = isUnread;
                break;
            case 'important':
                shouldShow = isImportant;
                break;
            case 'campaigns':
                shouldShow = isCampaign;
                break;
        }

        notification.style.display = shouldShow ? 'flex' : 'none';
    });
}

// Marcar como lida
function markAsRead(notificationId) {
    const notification = document.querySelector(`[data-id="${notificationId}"]`);
    if (notification) {
        notification.classList.remove('unread');
        notification.classList.add('read');

        // Remover indicador de não lida
        const indicator = notification.querySelector('.unread-indicator');
        if (indicator) {
            indicator.remove();
        }

        updateStats();

        // Animação de feedback
        notification.style.transform = 'scale(0.98)';
        setTimeout(() => {
            notification.style.transform = 'scale(1)';
        }, 150);
    }
}

// Marcar todas como lidas
function markAllAsRead() {
    if (confirm('Deseja marcar todas as notificações como lidas?')) {
        document.querySelectorAll('.notification-item.unread').forEach(notification => {
            notification.classList.remove('unread');
            notification.classList.add('read');

            const indicator = notification.querySelector('.unread-indicator');
            if (indicator) {
                indicator.remove();
            }
        });

        updateStats();
        showToast('Todas as notificações foram marcadas como lidas!', 'success');
    }
}

// Limpar todas as notificações
function clearAllNotifications() {
    if (confirm('Deseja limpar todas as notificações? Esta ação não pode ser desfeita.')) {
        document.querySelectorAll('.notification-item').forEach(notification => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(-100%)';
            setTimeout(() => {
                notification.remove();
            }, 300);
        });

        setTimeout(() => {
            updateStats();
            showToast('Todas as notificações foram removidas!', 'info');
        }, 300);
    }
}

// Atualizar estatísticas
function updateStats() {
    const total = document.querySelectorAll('.notification-item').length;
    const unread = document.querySelectorAll('.notification-item.unread').length;
    const important = document.querySelectorAll('.notification-item.critical, .notification-item.result').length;
    const today = document.querySelectorAll('.notification-item').length; // Simplificado

    document.getElementById('totalNotifications').textContent = total;
    document.getElementById('unreadNotifications').textContent = unread;
    document.getElementById('importantNotifications').textContent = important;
    document.getElementById('todayNotifications').textContent = Math.min(today, 5);
}

// Visualizar detalhes
function viewDetails(notificationId) {
    const modal = new bootstrap.Modal(document.getElementById('detailsModal'));

    // Conteúdo específico baseado no ID
    const details = {
        1: {
            title: 'Estoque Crítico - Tipo O+',
            content: `
                    <div class="alert alert-danger">
                        <h6><i class="fas fa-exclamation-triangle me-2"></i>Situação Crítica</h6>
                        <p>O estoque de sangue tipo O+ está em nível crítico com apenas 4 unidades disponíveis.</p>
                    </div>
                    <h6>Detalhes do Estoque:</h6>
                    <ul>
                        <li>Tipo sanguíneo: O+ (Doador Universal para Rh+)</li>
                        <li>Quantidade atual: 4 unidades</li>
                        <li>Nível mínimo recomendado: 15 unidades</li>
                        <li>Demanda média diária: 3-5 unidades</li>
                    </ul>
                    <h6>Ações Recomendadas:</h6>
                    <ul>
                        <li>Ativar campanha de doação urgente</li>
                        <li>Contatar doadores tipo O+ cadastrados</li>
                        <li>Coordenar com outros hemocentros</li>
                    </ul>
                `,
            action: 'Ativar Campanha'
        }
    };

    const detail = details[notificationId] || {
        title: 'Detalhes da Notificação',
        content: '<p>Informações detalhadas sobre esta notificação.</p>',
        action: 'OK'
    };

    document.getElementById('modalTitle').textContent = detail.title;
    document.getElementById('modalBody').innerHTML = detail.content;
    document.getElementById('modalAction').textContent = detail.action;

    modal.show();
    markAsRead(notificationId);
}

// Outras funções de ação
function viewCampaign(id) {
    window.location.href = 'doador_campanha.html';
}

function viewAppointment(id) {
    window.location.href = 'doador_agendamento.html';
}

function scheduleNewDonation() {
    window.location.href = 'doador_agendamento.html';
}

function viewResults(id) {
    showToast('Redirecionando para área de resultados...', 'info');
}

function viewImpact(id) {
    showToast('Visualizando impacto das suas doações...', 'success');
}

function viewUpdate(id) {
    showToast('Visualizando novidades do sistema...', 'info');
}

function viewDonation(id) {
    showToast('Abrindo certificado de doação...', 'success');
}

// Atualizar notificações
function refreshNotifications() {
    const btn = document.querySelector('.floating-btn i');
    btn.classList.add('fa-spin');

    setTimeout(() => {
        btn.classList.remove('fa-spin');
        showToast('Notificações atualizadas!', 'success');
    }, 1000);
}

// Mostrar toast
function showToast(message, type = 'info') {
    // Criar elemento de toast
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'times' : 'info'}-circle me-2"></i>
            ${message}
        `;

    // Adicionar ao body
    document.body.appendChild(toast);

    // Mostrar com animação
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);

    // Remover após 3 segundos
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}