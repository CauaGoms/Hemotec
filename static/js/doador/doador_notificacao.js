// Variáveis globais
let currentFilter = 'all';
let allNotifications = [];

// Inicializar página
document.addEventListener('DOMContentLoaded', function () {
    loadNotifications();

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

// Carregar notificações do banco de dados
async function loadNotifications() {
    try {
        const response = await fetch('/api/notificacoes');
        const data = await response.json();
        allNotifications = data.notificacoes;
        renderNotifications();
        updateStats();
    } catch (error) {
        console.error('Erro ao carregar notificações:', error);
        showToast('Erro ao carregar notificações', 'error');
    }
}

// Renderizar notificações
function renderNotifications() {
    const container = document.getElementById('notifications-list');
    const noNotifications = document.getElementById('no-notifications');

    // Filtrar notificações
    let filteredNotifications = allNotifications;

    if (currentFilter === 'unread') {
        filteredNotifications = allNotifications.filter(n => n.status === 1);
    } else if (currentFilter === 'important') {
        filteredNotifications = allNotifications.filter(n => n.tipo.toLowerCase() === 'estoque');
    } else if (currentFilter === 'campaigns') {
        filteredNotifications = allNotifications.filter(n => n.tipo.toLowerCase() === 'campanha');
    }

    // Se não há notificações
    if (filteredNotifications.length === 0) {
        container.innerHTML = '';
        noNotifications.style.display = 'block';
        return;
    }

    noNotifications.style.display = 'none';

    // Renderizar cada notificação
    container.innerHTML = filteredNotifications.map(notif => {
        const isUnread = notif.status === 1;
        const isImportant = notif.tipo.toLowerCase() === 'estoque';
        const typeClass = isImportant ? 'critical' :
            notif.tipo.toLowerCase() === 'campanha' ? 'campaign' :
                notif.tipo.toLowerCase() === 'agendamento' ? 'success' : 'info';
        const icon = isImportant ? 'exclamation-triangle' :
            notif.tipo.toLowerCase() === 'campanha' ? 'bullhorn' :
                notif.tipo.toLowerCase() === 'agendamento' ? 'calendar-check' : 'bell';

        const dataFormatada = formatarData(notif.data_envio);

        return `
            <div class="notification-item ${typeClass} ${isUnread ? 'unread' : 'read'}" data-type="${isImportant ? 'important' : notif.tipo.toLowerCase()}" data-id="${notif.cod_notificacao}">
                <div class="notification-icon">
                    <i class="fas fa-${icon}"></i>
                </div>
                <div class="notification-content">
                    <div class="notification-header">
                        <h5>${notif.titulo}</h5>
                        <div class="notification-meta">
                            <span class="badge bg-secondary">${notif.tipo}</span>
                            <span class="time">${dataFormatada}</span>
                        </div>
                    </div>
                    <p>${notif.mensagem}</p>
                    <div class="notification-actions">
                        ${isUnread ? `<button class="btn btn-sm btn-outline-secondary" onclick="markAsRead(${notif.cod_notificacao})">Marcar como Lida</button>` : ''}
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteNotification(${notif.cod_notificacao})">Excluir</button>
                    </div>
                </div>
                <div class="notification-status">
                    ${isUnread ? '<div class="unread-indicator"></div>' : ''}
                </div>
            </div>
        `;
    }).join('');
}

// Formatar data
function formatarData(dataStr) {
    const data = new Date(dataStr);
    const agora = new Date();
    const diffMs = agora - data;
    const diffHoras = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDias = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffHoras < 1) {
        return 'Agora mesmo';
    } else if (diffHoras < 24) {
        return `Há ${diffHoras} hora${diffHoras > 1 ? 's' : ''}`;
    } else if (diffDias === 1) {
        return 'Ontem';
    } else if (diffDias < 7) {
        return `Há ${diffDias} dias`;
    } else {
        return data.toLocaleDateString('pt-BR');
    }
}

// Filtrar notificações
function filterNotifications(filter) {
    currentFilter = filter;

    // Atualizar botões de filtro
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-filter="${filter}"]`).classList.add('active');

    renderNotifications();
}

// Marcar como lida
async function markAsRead(notificationId) {
    try {
        const response = await fetch(`/api/notificacoes/${notificationId}/marcar-lida`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (data.success) {
            // Atualizar localmente
            const notif = allNotifications.find(n => n.cod_notificacao === notificationId);
            if (notif) {
                notif.status = 0;
            }

            renderNotifications();
            updateStats();
            showToast('Notificação marcada como lida!', 'success');
        } else {
            showToast('Erro ao marcar notificação como lida', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showToast('Erro ao marcar notificação como lida', 'error');
    }
}

// Marcar todas como lidas
async function markAllAsRead() {
    if (!confirm('Deseja marcar todas as notificações como lidas?')) {
        return;
    }

    try {
        const response = await fetch('/api/notificacoes/marcar-todas-lidas', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (data.success) {
            // Atualizar localmente
            allNotifications.forEach(n => n.status = 0);

            renderNotifications();
            updateStats();
            showToast('Todas as notificações foram marcadas como lidas!', 'success');
        } else {
            showToast('Erro ao marcar notificações como lidas', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showToast('Erro ao marcar notificações como lidas', 'error');
    }
}

// Deletar notificação
async function deleteNotification(notificationId) {
    if (!confirm('Deseja excluir esta notificação?')) {
        return;
    }

    try {
        const response = await fetch(`/api/notificacoes/${notificationId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (data.success) {
            // Remover localmente
            allNotifications = allNotifications.filter(n => n.cod_notificacao !== notificationId);

            renderNotifications();
            updateStats();
            showToast('Notificação excluída!', 'success');
        } else {
            showToast('Erro ao excluir notificação', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showToast('Erro ao excluir notificação', 'error');
    }
}

// Limpar todas as notificações
async function clearAllNotifications() {
    if (!confirm('Deseja limpar todas as notificações? Esta ação não pode ser desfeita.')) {
        return;
    }

    try {
        const response = await fetch('/api/notificacoes/limpar-todas', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (data.success) {
            allNotifications = [];
            renderNotifications();
            updateStats();
            showToast('Todas as notificações foram removidas!', 'info');
        } else {
            showToast('Erro ao limpar notificações', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showToast('Erro ao limpar notificações', 'error');
    }
}

// Atualizar estatísticas
function updateStats() {
    const total = allNotifications.length;
    const unread = allNotifications.filter(n => n.status === 1).length;
    const important = allNotifications.filter(n => n.tipo.toLowerCase() === 'estoque').length;

    // Contar notificações de hoje
    const hoje = new Date();
    hoje.setHours(0, 0, 0, 0);
    const today = allNotifications.filter(n => {
        const dataNotif = new Date(n.data_envio);
        dataNotif.setHours(0, 0, 0, 0);
        return dataNotif.getTime() === hoje.getTime();
    }).length;

    document.getElementById('totalNotifications').textContent = total;
    document.getElementById('unreadNotifications').textContent = unread;
    document.getElementById('importantNotifications').textContent = important;
    document.getElementById('todayNotifications').textContent = today;
}

// Atualizar notificações
async function refreshNotifications() {
    const btn = document.querySelector('.floating-btn i');
    btn.classList.add('fa-spin');

    await loadNotifications();

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