// Confirmar Redefinição de Senha - JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const loginBtn = document.querySelector('.btn-recovery');
    const container = document.querySelector('.recovery-container');
    
    // Função para adicionar animação de entrada
    function addEntryAnimation() {
        container.style.opacity = '0';
        container.style.transform = 'translateY(20px)';
        container.style.transition = 'all 0.5s ease';
        
        setTimeout(() => {
            container.style.opacity = '1';
            container.style.transform = 'translateY(0)';
        }, 100);
    }
    
    // Função para adicionar efeito de confete (celebração)
    function createConfetti() {
        const colors = ['#e02020', '#ff4040', '#28a745', '#ffc107', '#17a2b8'];
        const confettiCount = 50;
        
        for (let i = 0; i < confettiCount; i++) {
            const confetti = document.createElement('div');
            confetti.style.position = 'fixed';
            confetti.style.width = '10px';
            confetti.style.height = '10px';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.left = Math.random() * window.innerWidth + 'px';
            confetti.style.top = '-10px';
            confetti.style.zIndex = '9999';
            confetti.style.pointerEvents = 'none';
            confetti.style.borderRadius = '50%';
            
            document.body.appendChild(confetti);
            
            // Animação de queda
            const fallDuration = Math.random() * 3000 + 2000;
            const horizontalMovement = (Math.random() - 0.5) * 200;
            
            confetti.animate([
                {
                    transform: 'translateY(0px) translateX(0px) rotate(0deg)',
                    opacity: 1
                },
                {
                    transform: `translateY(${window.innerHeight + 20}px) translateX(${horizontalMovement}px) rotate(360deg)`,
                    opacity: 0
                }
            ], {
                duration: fallDuration,
                easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
            }).onfinish = () => {
                confetti.remove();
            };
        }
    }
    
    // Função para mostrar mensagem de boas-vindas personalizada
    function showWelcomeMessage() {
        const hour = new Date().getHours();
        let greeting = '';
        
        if (hour < 12) {
            greeting = 'Bom dia!';
        } else if (hour < 18) {
            greeting = 'Boa tarde!';
        } else {
            greeting = 'Boa noite!';
        }
        
        const welcomeDiv = document.createElement('div');
        welcomeDiv.className = 'welcome-message mt-3 p-3 bg-light rounded';
        welcomeDiv.innerHTML = `
            <div class="text-center">
                <h5 class="text-success mb-2">${greeting}</h5>
                <p class="mb-0 text-muted">
                    Sua conta está mais segura agora. Lembre-se de manter sua senha em local seguro.
                </p>
            </div>
        `;
        
        container.appendChild(welcomeDiv);
        
        // Animação de entrada da mensagem
        welcomeDiv.style.opacity = '0';
        welcomeDiv.style.transform = 'translateY(10px)';
        welcomeDiv.style.transition = 'all 0.3s ease';
        
        setTimeout(() => {
            welcomeDiv.style.opacity = '1';
            welcomeDiv.style.transform = 'translateY(0)';
        }, 1000);
    }
    
    // Função para adicionar dicas de segurança
    function showSecurityTips() {
        const tipsDiv = document.createElement('div');
        tipsDiv.className = 'security-tips mt-3';
        tipsDiv.innerHTML = `
            <div class="accordion" id="securityAccordion">
                <div class="accordion-item">
                    <h2 class="accordion-header">
                        <button class="accordion-button collapsed" type="button" 
                                data-bs-toggle="collapse" data-bs-target="#securityTips">
                            <i class="fas fa-shield-alt me-2 text-primary"></i>
                            Dicas de Segurança
                        </button>
                    </h2>
                    <div id="securityTips" class="accordion-collapse collapse">
                        <div class="accordion-body">
                            <ul class="list-unstyled mb-0">
                                <li class="mb-2">
                                    <i class="fas fa-check text-success me-2"></i>
                                    Nunca compartilhe sua senha com terceiros
                                </li>
                                <li class="mb-2">
                                    <i class="fas fa-check text-success me-2"></i>
                                    Use senhas diferentes para cada serviço
                                </li>
                                <li class="mb-2">
                                    <i class="fas fa-check text-success me-2"></i>
                                    Altere sua senha regularmente
                                </li>
                                <li class="mb-0">
                                    <i class="fas fa-check text-success me-2"></i>
                                    Sempre faça logout ao usar computadores públicos
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        container.appendChild(tipsDiv);
    }
    
    // Função para adicionar contador regressivo para redirecionamento automático
    function addAutoRedirectCountdown() {
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
            countdownElement.textContent = timeLeft;
            
            if (timeLeft <= 0) {
                clearInterval(countdownInterval);
                window.location.href = '/login';
            }
        }, 1000);
        
        // Para o countdown se o usuário clicar no botão
        loginBtn.addEventListener('click', () => {
            clearInterval(countdownInterval);
        });
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
    
    // Função para adicionar botão de feedback
    function addFeedbackButton() {
        const feedbackDiv = document.createElement('div');
        feedbackDiv.className = 'feedback-section mt-4 text-center';
        feedbackDiv.innerHTML = `
            <div class="border-top pt-3">
                <p class="text-muted mb-2">Como foi sua experiência?</p>
                <div class="btn-group" role="group">
                    <button type="button" class="btn btn-outline-success btn-sm feedback-btn" data-rating="positive">
                        <i class="fas fa-thumbs-up me-1"></i>Ótima
                    </button>
                    <button type="button" class="btn btn-outline-warning btn-sm feedback-btn" data-rating="neutral">
                        <i class="fas fa-meh me-1"></i>Regular
                    </button>
                    <button type="button" class="btn btn-outline-danger btn-sm feedback-btn" data-rating="negative">
                        <i class="fas fa-thumbs-down me-1"></i>Ruim
                    </button>
                </div>
                <div id="feedbackMessage" class="mt-2" style="display: none;">
                    <small class="text-success">
                        <i class="fas fa-heart me-1"></i>Obrigado pelo seu feedback!
                    </small>
                </div>
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
                if (rating === 'positive') this.classList.add('btn-success');
                else if (rating === 'neutral') this.classList.add('btn-warning');
                else this.classList.add('btn-danger');
                
                // Mostra mensagem de agradecimento
                document.getElementById('feedbackMessage').style.display = 'block';
            });
        });
    }
    
    // Inicialização da página
    function initializePage() {
        // Adiciona animação de entrada
        addEntryAnimation();
        
        // Cria efeito de confete após um pequeno delay
        setTimeout(createConfetti, 500);
        
        // Adiciona efeito de pulso no ícone
        addSuccessIconPulse();
        
        // Mostra mensagem de boas-vindas
        setTimeout(showWelcomeMessage, 1000);
        
        // Adiciona dicas de segurança
        setTimeout(showSecurityTips, 1500);
        
        // Adiciona botão de feedback
        setTimeout(addFeedbackButton, 2000);
        
        // Adiciona contador regressivo (opcional)
        setTimeout(addAutoRedirectCountdown, 2500);
        
        // Rastreia evento de sucesso
        trackSuccessEvent();
    }
    
    // Event listener para o botão de login
    loginBtn.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Adiciona efeito de loading
        this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Redirecionando...';
        this.disabled = true;
        
        // Redireciona após um pequeno delay
        setTimeout(() => {
            window.location.href = '/login';
        }, 1000);
    });
    
    // Inicializa a página
    initializePage();
    
    // Adiciona listener para tecla Enter
    document.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            loginBtn.click();
        }
    });
});

