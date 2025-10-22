// Variáveis globais
let currentFilter = 'all';
let allNotifications = [];
let currentPage = 1;
const itemsPerPage = 10;

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
        const response = await fetch('/api/administrador/notificacoes');
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
        document.querySelector('.pagination-container').style.display = 'none';
        return;
    }

    noNotifications.style.display = 'none';

    // Calcular paginação
    const totalPages = Math.ceil(filteredNotifications.length / itemsPerPage);
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedNotifications = filteredNotifications.slice(startIndex, endIndex);

    // Renderizar cada notificação
    container.innerHTML = paginatedNotifications.map(notif => {
        const isUnread = notif.status === 1;
        const tipoLower = notif.tipo.toLowerCase();
        const isImportant = tipoLower === 'estoque';

        // Definir classe e ícone baseado no tipo
        let typeClass, icon;

        if (isImportant) {
            typeClass = 'critical';
            icon = 'exclamation-triangle';
        } else if (tipoLower === 'campanha') {
            typeClass = 'campaign';
            icon = 'bullhorn';
        } else if (tipoLower === 'agendamento') {
            typeClass = 'appointment';
            icon = 'calendar-alt';
        } else if (tipoLower === 'agradecimento') {
            typeClass = 'thanks';
            icon = 'heart';
        } else {
            typeClass = 'info';
            icon = 'bell';
        }

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

    // Renderizar paginação
    renderPagination(totalPages);
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
    currentPage = 1; // Resetar para primeira página ao filtrar

    // Atualizar botões de filtro
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-filter="${filter}"]`).classList.add('active');

    renderNotifications();
}

// Renderizar paginação
function renderPagination(totalPages) {
    const paginationContainer = document.querySelector('.pagination ul');

    if (totalPages <= 1) {
        document.querySelector('.pagination-container').style.display = 'none';
        return;
    }

    document.querySelector('.pagination-container').style.display = 'block';

    let paginationHTML = '';

    // Botão Anterior
    if (currentPage > 1) {
        paginationHTML += `
            <li class="page-item">
                <a class="page-link" href="#" onclick="goToPage(${currentPage - 1}); return false;">Anterior</a>
            </li>
        `;
    }

    // Números das páginas
    const maxVisiblePages = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
    let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

    // Ajustar startPage se estiver no final
    if (endPage - startPage < maxVisiblePages - 1) {
        startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }

    // Primeira página se não estiver visível
    if (startPage > 1) {
        paginationHTML += `
            <li class="page-item">
                <a class="page-link" href="#" onclick="goToPage(1); return false;">1</a>
            </li>
        `;
        if (startPage > 2) {
            paginationHTML += `
                <li class="page-item disabled">
                    <span class="page-link">...</span>
                </li>
            `;
        }
    }

    // Páginas numeradas
    for (let i = startPage; i <= endPage; i++) {
        paginationHTML += `
            <li class="page-item ${i === currentPage ? 'active' : ''}">
                <a class="page-link" href="#" onclick="goToPage(${i}); return false;">${i}</a>
            </li>
        `;
    }

    // Última página se não estiver visível
    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            paginationHTML += `
                <li class="page-item disabled">
                    <span class="page-link">...</span>
                </li>
            `;
        }
        paginationHTML += `
            <li class="page-item">
                <a class="page-link" href="#" onclick="goToPage(${totalPages}); return false;">${totalPages}</a>
            </li>
        `;
    }

    // Botão Próximo
    if (currentPage < totalPages) {
        paginationHTML += `
            <li class="page-item">
                <a class="page-link" href="#" onclick="goToPage(${currentPage + 1}); return false;">Próximo</a>
            </li>
        `;
    }

    paginationContainer.innerHTML = paginationHTML;
}

// Ir para página específica
function goToPage(page) {
    currentPage = page;
    renderNotifications();

    // Scroll suave para o topo das notificações
    document.querySelector('.notifications-container').scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// Marcar como lida
async function markAsRead(notificationId) {
    try {
        const response = await fetch(`/api/administrador/notificacoes/${notificationId}/marcar-lida`, {
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
    const confirmed = await showConfirmDialog(
        'Marcar todas como lidas?',
        'Todas as notificações não lidas serão marcadas como lidas.',
        'Confirmar'
    );

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch('/api/administrador/notificacoes/marcar-todas-lidas', {
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
    const confirmed = await showConfirmDialog(
        'Excluir notificação?',
        'Esta ação não pode ser desfeita.',
        'Excluir'
    );

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(`/api/administrador/notificacoes/${notificationId}`, {
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
    const confirmed = await showConfirmDialog(
        'Limpar todas as notificações?',
        'Todas as notificações serão removidas permanentemente. Esta ação não pode ser desfeita.',
        'Limpar Tudo'
    );

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch('/api/administrador/notificacoes/limpar-todas', {
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

// Mostrar dialog de confirmação personalizado
function showConfirmDialog(title, message, confirmText = 'Confirmar') {
    return new Promise((resolve) => {
        // Remover dialog anterior se existir
        const existingDialog = document.getElementById('custom-confirm-dialog');
        if (existingDialog) {
            existingDialog.remove();
        }

        // Criar dialog
        const dialog = document.createElement('div');
        dialog.id = 'custom-confirm-dialog';
        dialog.className = 'custom-confirm-dialog';
        dialog.innerHTML = `
            <div class="confirm-dialog-content">
                <div class="confirm-dialog-icon">
                    <i class="fas fa-question-circle"></i>
                </div>
                <div class="confirm-dialog-body">
                    <h5>${title}</h5>
                    <p>${message}</p>
                </div>
                <div class="confirm-dialog-actions">
                    <button class="btn-cancel">
                        <i class="fas fa-times me-2"></i>Cancelar
                    </button>
                    <button class="btn-confirm">
                        <i class="fas fa-check me-2"></i>${confirmText}
                    </button>
                </div>
            </div>
        `;

        // Adicionar estilos
        if (!document.getElementById('confirm-dialog-styles')) {
            const styles = document.createElement('style');
            styles.id = 'confirm-dialog-styles';
            styles.textContent = `
                .custom-confirm-dialog {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    z-index: 10000;
                    animation: slideInRight 0.4s ease-out;
                }

                @keyframes slideInRight {
                    from {
                        transform: translateX(100%);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }

                @keyframes slideOutRight {
                    from {
                        transform: translateX(0);
                        opacity: 1;
                    }
                    to {
                        transform: translateX(100%);
                        opacity: 0;
                    }
                }

                .custom-confirm-dialog.closing {
                    animation: slideOutRight 0.3s ease-in forwards;
                }

                .confirm-dialog-content {
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
                    padding: 25px;
                    min-width: 380px;
                    max-width: 450px;
                    border-top: 4px solid #dc3545;
                }

                .confirm-dialog-icon {
                    text-align: center;
                    margin-bottom: 15px;
                }

                .confirm-dialog-icon i {
                    font-size: 48px;
                    color: #dc3545;
                    animation: pulse 2s infinite;
                }

                @keyframes pulse {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.1); }
                }

                .confirm-dialog-body {
                    text-align: center;
                    margin-bottom: 20px;
                }

                .confirm-dialog-body h5 {
                    color: #333;
                    font-weight: 600;
                    font-size: 20px;
                    margin-bottom: 10px;
                }

                .confirm-dialog-body p {
                    color: #666;
                    font-size: 15px;
                    margin: 0;
                    line-height: 1.5;
                }

                .confirm-dialog-actions {
                    display: flex;
                    gap: 12px;
                    justify-content: center;
                }

                .confirm-dialog-actions button {
                    padding: 10px 24px;
                    border: none;
                    border-radius: 8px;
                    font-weight: 600;
                    font-size: 14px;
                    cursor: pointer;
                    transition: all 0.3s;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                }

                .confirm-dialog-actions .btn-cancel {
                    background: #6c757d;
                    color: white;
                }

                .confirm-dialog-actions .btn-cancel:hover {
                    background: #5a6268;
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(108, 117, 125, 0.3);
                }

                .confirm-dialog-actions .btn-confirm {
                    background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
                    color: white;
                }

                .confirm-dialog-actions .btn-confirm:hover {
                    background: linear-gradient(135deg, #c82333 0%, #bd2130 100%);
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(220, 53, 69, 0.4);
                }

                @media (max-width: 768px) {
                    .custom-confirm-dialog {
                        left: 20px;
                        right: 20px;
                        top: 20px;
                    }
                    
                    .confirm-dialog-content {
                        min-width: auto;
                        max-width: none;
                    }
                }
            `;
            document.head.appendChild(styles);
        }

        // Adicionar ao body
        document.body.appendChild(dialog);

        // Event listeners
        const btnCancel = dialog.querySelector('.btn-cancel');
        const btnConfirm = dialog.querySelector('.btn-confirm');

        const closeDialog = (confirmed) => {
            dialog.classList.add('closing');
            setTimeout(() => {
                dialog.remove();
                resolve(confirmed);
            }, 300);
        };

        btnCancel.onclick = () => closeDialog(false);
        btnConfirm.onclick = () => closeDialog(true);

        // Fechar com ESC
        const escHandler = (e) => {
            if (e.key === 'Escape') {
                closeDialog(false);
                document.removeEventListener('keydown', escHandler);
            }
        };
        document.addEventListener('keydown', escHandler);
    });
}
