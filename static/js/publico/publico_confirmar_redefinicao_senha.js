// Confirmar Redefinição de Senha - JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const loginBtn = document.querySelector('.btn-recovery');
    const container = document.querySelector('.recovery-container');
    
    // Função para adicionar contador regressivo para redirecionamento automático
    function addAutoRedirectCountdown() {
        if (!container) return; // Garante que o container existe
        const countdownDiv = document.createElement('div');
        countdownDiv.className = 'auto-redirect mt-3 text-center';
        countdownDiv.innerHTML = `
            <small class="text-muted">
                <i class="fas fa-clock me-1"></i>
                Redirecionamento automático em <span id="countdown">30</span> segundos
            </small>
        `;
        
        container.appendChild(countdownDiv);
        
        let timeLeft = 30;
        const countdownElement = document.getElementById('countdown');
        
        const countdownInterval = setInterval(() => {
            timeLeft--;
            if (countdownElement) {
                countdownElement.textContent = timeLeft;
            }
            
            if (timeLeft <= 0) {
                clearInterval(countdownInterval);
                window.location.href = '/login';
            }
        }, 1000);
        
        // Para o countdown se o usuário clicar no botão
        if (loginBtn) {
            loginBtn.addEventListener('click', () => {
                clearInterval(countdownInterval);
            });
        }
    }
    
    // Função para adicionar efeito de pulso no ícone de sucesso
    function addSuccessIconPulse() {
        const successIcon = document.querySelector('.success-icon i');
        if (successIcon) {
            successIcon.style.animation = 'pulse 2s infinite';
            
            // Adiciona CSS para animação de pulso
            const style = document.createElement('style');
            style.textContent = `
                @keyframes pulse {
                    0% { transform: scale(1); }
                    50% { transform: scale(1.1); }
                    100% { transform: scale(1); }
                }
            `;
            document.head.appendChild(style);
        }
    }
    
    // Função para rastrear evento de sucesso (analytics)
    function trackSuccessEvent() {
        // Simula envio de evento para analytics
        console.log('Evento rastreado: Redefinição de senha concluída com sucesso');
        
        // Aqui você poderia integrar com Google Analytics, Mixpanel, etc.
        // Exemplo: gtag('event', 'password_reset_success', { ... });
    }

    // Função para adicionar e gerenciar o bloco de feedback
    function addFeedbackSection() {
        if (!container) return; // Garante que o container existe
        const feedbackDiv = document.createElement('div');
        feedbackDiv.className = 'feedback-section mt-4 text-center';
        feedbackDiv.innerHTML = `
            <h5>O quão útil foi esta página?</h5>
            <div class="d-flex justify-content-center gap-2 mt-2">
                <button class="btn btn-outline-success feedback-btn" data-rating="positive">
                    <i class="fas fa-thumbs-up"></i>
                </button>
                <button class="btn btn-outline-warning feedback-btn" data-rating="neutral">
                    <i class="fas fa-meh"></i>
                </button>
                <button class="btn btn-outline-danger feedback-btn" data-rating="negative">
                    <i class="fas fa-thumbs-down"></i>
                </button>
            </div>
            <div id="feedbackMessage" class="mt-3 text-success" style="display: none;">
                Obrigado pelo seu feedback!
            </div>
        `;
        container.appendChild(feedbackDiv);
        
        // Event listeners para botões de feedback
        const feedbackButtons = document.querySelectorAll('.feedback-btn');
        feedbackButtons.forEach(button => {
            button.addEventListener('click', function() {
                const rating = this.dataset.rating;
                console.log('Feedback enviado:', rating);
                
                // Desabilita todos os botões
                feedbackButtons.forEach(btn => {
                    btn.disabled = true;
                    btn.classList.remove('btn-outline-success', 'btn-outline-warning', 'btn-outline-danger');
                    btn.classList.add('btn-secondary');
                });
                
                // Destaca o botão clicado
                this.classList.remove('btn-secondary');
                if (rating === 'positive') {
                    this.classList.add('btn-success');
                } else if (rating === 'neutral') {
                    this.classList.add('btn-warning');
                } else {
                    this.classList.add('btn-danger');
                }
                
                // Mostra mensagem de agradecimento
                document.getElementById('feedbackMessage').style.display = 'block';
            });
        });
    }

    // Chamadas das funções para executá-las no carregamento da página
    if (container) {
        showSecurityTips();
        addAutoRedirectCountdown();
        addSuccessIconPulse(); // Assume que o ícone de sucesso já existe no HTML
        trackSuccessEvent();
        addFeedbackSection();
    } else {
        console.error('O elemento com a classe ".recovery-container" não foi encontrado.');
    }
});