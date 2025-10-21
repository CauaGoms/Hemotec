// ========================================
// COLABORADOR INÍCIO - JAVASCRIPT
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funções
    initDateTime();
    loadDashboardData();
    
    // Atualizar relógio a cada segundo para hora em tempo real
    setInterval(initDateTime, 1000);
});

// ========================================
// FUNÇÃO: EXIBIR DATA E HORA ATUAL
// ======================================== 
function initDateTime() {
    const dateElement = document.getElementById('current-date');
    const timeElement = document.getElementById('current-time');
    
    if (!dateElement || !timeElement) return;

    const now = new Date();
    
    // Formatar data
    const dateOptions = {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };
    
    const formattedDate = now.toLocaleDateString('pt-BR', dateOptions);
    dateElement.textContent = formattedDate.charAt(0).toUpperCase() + formattedDate.slice(1);
    
    // Formatar hora
    const timeOptions = {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    };
    
    const formattedTime = now.toLocaleTimeString('pt-BR', timeOptions);
    timeElement.textContent = formattedTime;
}

// ========================================
// FUNÇÃO: CARREGAR DADOS DO DASHBOARD
// ========================================
async function loadDashboardData() {
    try {
        // Carregar estatísticas
        await loadStatistics();
        
        // Carregar agendamentos de hoje
        await loadTodayAppointments();
        
        // Carregar doações em andamento
        await loadOngoingDonations();
        
        // Carregar campanhas em destaque
        await loadFeaturedCampaigns();
        
        // Carregar notificações recentes
        await loadRecentNotifications();
    } catch (error) {
        console.error('Erro ao carregar dados do dashboard:', error);
        showErrorMessage('Erro ao carregar dados. Por favor, recarregue a página.');
    }
}

// ========================================
// FUNÇÃO: CARREGAR ESTATÍSTICAS
// ========================================
async function loadStatistics() {
    try {
        // TODO: Substituir por chamada real à API
        // const response = await fetch('/api/colaborador/estatisticas');
        // const data = await response.json();
        
        // Dados simulados (remover quando integrar com backend)
        const stats = {
            agendamentosHoje: 15,
            doacoesPendentes: 8,
            campanhasAtivas: 3,
            notificacoesNovas: 5
        };
        
        // Atualizar contadores com animação
        animateCounter('agendamentos-hoje', stats.agendamentosHoje);
        animateCounter('doacoes-pendentes', stats.doacoesPendentes);
        animateCounter('campanhas-ativas', stats.campanhasAtivas);
        animateCounter('notificacoes-novas', stats.notificacoesNovas);
        
    } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
    }
}

// ========================================
// FUNÇÃO: ANIMAR CONTADORES
// ========================================
function animateCounter(elementId, targetValue, duration = 1000) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    let startValue = 0;
    const increment = targetValue / (duration / 16); // 60 FPS
    
    const timer = setInterval(() => {
        startValue += increment;
        if (startValue >= targetValue) {
            element.textContent = targetValue;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(startValue);
        }
    }, 16);
}

// ========================================
// FUNÇÃO: CARREGAR AGENDAMENTOS DE HOJE
// ========================================
async function loadTodayAppointments() {
    try {
        // TODO: Substituir por chamada real à API
        // const response = await fetch('/api/colaborador/agendamentos/hoje');
        // const agendamentos = await response.json();
        
        // Dados simulados (remover quando integrar com backend)
        const agendamentos = [
            {
                id: 1,
                horario: '09:00',
                doador: 'Maria Silva',
                tipoSanguineo: 'O+',
                status: 'confirmado'
            },
            {
                id: 2,
                horario: '10:30',
                doador: 'João Santos',
                tipoSanguineo: 'A+',
                status: 'pendente'
            },
            {
                id: 3,
                horario: '14:00',
                doador: 'Ana Costa',
                tipoSanguineo: 'B-',
                status: 'confirmado'
            }
        ];
        
        const container = document.getElementById('agendamentos-hoje-lista');
        const badge = document.getElementById('total-agendamentos-hoje');
        
        if (agendamentos && agendamentos.length > 0) {
            container.innerHTML = '';
            badge.textContent = agendamentos.length;
            
            agendamentos.forEach(agendamento => {
                const item = createAppointmentItem(agendamento);
                container.appendChild(item);
            });
        }
        
    } catch (error) {
        console.error('Erro ao carregar agendamentos:', error);
    }
}

// ========================================
// FUNÇÃO: CRIAR ITEM DE AGENDAMENTO
// ========================================
function createAppointmentItem(agendamento) {
    const div = document.createElement('div');
    div.className = 'agenda-item';
    div.onclick = () => window.location.href = `/colaborador/agendamento`;
    
    div.innerHTML = `
        <div class="agenda-item-time">
            <i class="fas fa-clock me-1"></i>${agendamento.horario}
        </div>
        <div class="agenda-item-title">${agendamento.doador}</div>
        <div class="agenda-item-details">
            <span class="badge bg-danger me-2">${agendamento.tipoSanguineo}</span>
            <span class="badge ${agendamento.status === 'confirmado' ? 'bg-success' : 'bg-warning'}">
                ${agendamento.status === 'confirmado' ? 'Confirmado' : 'Pendente'}
            </span>
        </div>
    `;
    
    return div;
}

// ========================================
// FUNÇÃO: CARREGAR DOAÇÕES EM ANDAMENTO
// ========================================
async function loadOngoingDonations() {
    try {
        // TODO: Substituir por chamada real à API
        // const response = await fetch('/api/colaborador/doacoes/andamento');
        // const doacoes = await response.json();
        
        // Dados simulados (remover quando integrar com backend)
        const doacoes = [
            {
                id: 1,
                doador: 'Carlos Mendes',
                etapa: 'Triagem',
                horarioInicio: '08:45',
                tipoSanguineo: 'AB+'
            },
            {
                id: 2,
                doador: 'Beatriz Lima',
                etapa: 'Coleta',
                horarioInicio: '09:15',
                tipoSanguineo: 'O-'
            }
        ];
        
        const container = document.getElementById('doacoes-andamento-lista');
        const badge = document.getElementById('total-doacoes-andamento');
        
        if (doacoes && doacoes.length > 0) {
            container.innerHTML = '';
            badge.textContent = doacoes.length;
            
            doacoes.forEach(doacao => {
                const item = createDonationItem(doacao);
                container.appendChild(item);
            });
        }
        
    } catch (error) {
        console.error('Erro ao carregar doações:', error);
    }
}

// ========================================
// FUNÇÃO: CRIAR ITEM DE DOAÇÃO
// ========================================
function createDonationItem(doacao) {
    const div = document.createElement('div');
    div.className = 'agenda-item';
    div.style.borderLeftColor = '#ffc107';
    div.onclick = () => window.location.href = `/colaborador/doacoes`;
    
    div.innerHTML = `
        <div class="agenda-item-time" style="color: #ffc107;">
            <i class="fas fa-clock me-1"></i>${doacao.horarioInicio}
        </div>
        <div class="agenda-item-title">${doacao.doador}</div>
        <div class="agenda-item-details">
            <span class="badge bg-danger me-2">${doacao.tipoSanguineo}</span>
            <span class="badge bg-warning">${doacao.etapa}</span>
        </div>
    `;
    
    return div;
}

// ========================================
// FUNÇÃO: CARREGAR CAMPANHAS EM DESTAQUE
// ========================================
async function loadFeaturedCampaigns() {
    try {
        // TODO: Substituir por chamada real à API
        // const response = await fetch('/api/colaborador/campanhas/destaque');
        // const campanhas = await response.json();
        
        // Dados simulados (remover quando integrar com backend)
        const campanhas = [
            {
                id: 1,
                titulo: 'Campanha de Verão',
                descricao: 'Doe sangue e ajude a salvar vidas neste verão',
                imagem: '/static/img/campanha-verao.jpg',
                dataInicio: '2025-12-01',
                dataFim: '2026-02-28',
                status: 'ativa'
            },
            {
                id: 2,
                titulo: 'Doe Sangue, Salve Vidas',
                descricao: 'A sua doação pode fazer a diferença',
                imagem: '/static/img/campanha-solidaria.jpg',
                dataInicio: '2025-10-01',
                dataFim: '2025-12-31',
                status: 'ativa'
            }
        ];
        
        const container = document.getElementById('campanhas-destaque');
        
        if (campanhas && campanhas.length > 0) {
            container.innerHTML = '';
            
            campanhas.slice(0, 3).forEach(campanha => {
                const card = createCampaignCard(campanha);
                container.appendChild(card);
            });
        }
        
    } catch (error) {
        console.error('Erro ao carregar campanhas:', error);
    }
}

// ========================================
// FUNÇÃO: CRIAR CARD DE CAMPANHA
// ========================================
function createCampaignCard(campanha) {
    const div = document.createElement('div');
    div.className = 'col-lg-4 col-md-6';
    
    div.innerHTML = `
        <div class="campanha-card" onclick="window.location.href='/colaborador/campanha/detalhe/${campanha.id}'">
            <img src="${campanha.imagem}" alt="${campanha.titulo}" class="campanha-image" 
                 onerror="this.src='/static/img/placeholder-campanha.jpg'">
            <div class="campanha-body">
                <h4 class="campanha-title">${campanha.titulo}</h4>
                <p class="campanha-description">${campanha.descricao}</p>
                <div class="campanha-meta">
                    <span><i class="fas fa-calendar me-1"></i>${formatDate(campanha.dataInicio)} - ${formatDate(campanha.dataFim)}</span>
                    <span class="badge bg-success">${campanha.status}</span>
                </div>
            </div>
        </div>
    `;
    
    return div;
}

// ========================================
// FUNÇÃO: CARREGAR NOTIFICAÇÕES RECENTES
// ========================================
async function loadRecentNotifications() {
    // Notificações agora são renderizadas pelo servidor (Jinja2)
    // Esta função está desativada para não sobrescrever os dados do banco
    // Se precisar carregar via API, descomentar e ajustar conforme necessário
}

// ========================================
// FUNÇÕES UTILITÁRIAS
// ========================================

// Formatar data para exibição
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' });
}

// Exibir mensagem de erro
function showErrorMessage(message) {
    // TODO: Implementar sistema de toast/notificação
    console.error(message);
    alert(message);
}

// ========================================
// FUNÇÕES DE NAVEGAÇÃO RÁPIDA
// ========================================

function agendarDoacao() {
    window.location.href = '/colaborador/agendamento/adicionar';
}

function verCampanhas() {
    window.location.href = '/colaborador/campanha';
}

function registrarDoacao() {
    window.location.href = '/colaborador/doacoes/adicionar';
}

function realizarTriagem() {
    window.location.href = '/colaborador/doacoes/triagem';
}

function confirmarPresenca() {
    window.location.href = '/colaborador/agendamento';
}

function anexarResultados() {
    window.location.href = '/colaborador/doacoes';
}

function criarCampanha() {
    window.location.href = '/colaborador/campanha/adicionar';
}

function gerenciarHorarios() {
    window.location.href = '/colaborador/disponibilidade_coleta';
}