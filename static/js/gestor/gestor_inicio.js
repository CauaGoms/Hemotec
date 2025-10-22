/* ========================================
   GESTOR INÍCIO - JAVASCRIPT
   ======================================== */

/**
 * Atualizar data e hora em tempo real
 */
function atualizarDataHora() {
    const agora = new Date();
    
    // Formatar data
    const opcoes = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    const dataFormatada = agora.toLocaleDateString('pt-BR', opcoes);
    const dataPrimeira = dataFormatada.charAt(0).toUpperCase() + dataFormatada.slice(1);
    
    // Formatar hora
    const horaFormatada = agora.toLocaleTimeString('pt-BR', { 
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit'
    });
    
    // Atualizar elementos
    const elementoData = document.getElementById('current-date');
    const elementoHora = document.getElementById('current-time');
    
    if (elementoData) {
        elementoData.textContent = dataPrimeira;
    }
    if (elementoHora) {
        elementoHora.textContent = horaFormatada;
    }
}

/**
 * Inicializar quando o DOM estiver carregado
 */
document.addEventListener('DOMContentLoaded', function() {
    // Atualizar data/hora imediatamente
    atualizarDataHora();
    
    // Atualizar a cada segundo
    setInterval(atualizarDataHora, 1000);
    
    // Inicializar animações AOS se disponível
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 1000,
            once: false,
            easing: 'ease-in-out'
        });
    }
});

/**
 * Função para redirecionar para páginas
 */
function redirecionarPara(url) {
    window.location.href = url;
}

/**
 * Scroll suave
 */
function scrollSuave(id) {
    const elemento = document.getElementById(id);
    if (elemento) {
        elemento.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Formatador de data relativa (Há X horas, etc)
 */
function formatarDataRelativa(dataStr) {
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

/**
 * Animação de contagem para estatísticas
 */
function animarNumero(elemento, numero, duracao = 2000) {
    const inicio = 0;
    const incremento = numero / (duracao / 16);
    let atual = inicio;
    
    const intervalo = setInterval(() => {
        atual += incremento;
        if (atual >= numero) {
            elemento.textContent = numero;
            clearInterval(intervalo);
        } else {
            elemento.textContent = Math.floor(atual);
        }
    }, 16);
}

/**
 * Inicializar animações de números quando visíveis
 */
function inicializarAnimacoesNumeros() {
    const estatisticas = document.querySelectorAll('.stat-value');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.dataset.animado) {
                const numero = parseInt(entry.target.textContent);
                if (!isNaN(numero)) {
                    animarNumero(entry.target, numero);
                    entry.target.dataset.animado = 'true';
                }
            }
        });
    }, {
        threshold: 0.5
    });
    
    estatisticas.forEach(stat => {
        observer.observe(stat);
    });
}

/**
 * Validar e animar cards de ação
 */
function inicializarActionCards() {
    const cards = document.querySelectorAll('.action-card');
    
    cards.forEach(card => {
        card.addEventListener('click', function() {
            if (!this.classList.contains('disabled')) {
                // Adicionar efeito de clique
                this.style.transform = 'scale(0.98)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 200);
            }
        });
    });
}

/**
 * Tooltip customizado
 */
function inicializarTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Auto-refresh de notificações (opcional)
 */
function inicializarAutoRefreshNotificacoes(intervalo = 30000) {
    setInterval(() => {
        // Aqui você poderia fazer uma chamada AJAX para atualizar notificações
        // fetch('/api/notificacoes')
        //     .then(response => response.json())
        //     .then(data => atualizarNotificacoes(data));
    }, intervalo);
}

/**
 * Mostrar notificação de sucesso/erro
 */
function mostrarNotificacao(mensagem, tipo = 'success', duracao = 3000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${tipo} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${mensagem}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
    `;
    
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, duracao);
}

/**
 * Inicializar tudo quando o documento estiver pronto
 */
document.addEventListener('DOMContentLoaded', function() {
    inicializarActionCards();
    inicializarAnimacoesNumeros();
    inicializarTooltips();
    // inicializarAutoRefreshNotificacoes(); // Descomente se quiser auto-refresh
});

/**
 * Função helper para debug
 */
function debug(mensagem) {
    if (window.DEBUG_MODE) {
        console.log('[Gestor Início]', mensagem);
    }
}
