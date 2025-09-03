document.addEventListener('DOMContentLoaded', function() {
    initializePricingCards();
    setupCardInteractions();
    setupPlanSelection();
    setupScrollAnimations();
    setupParallaxEffect();
});

// Inicialização dos cards de preços
function initializePricingCards() {
    const cards = document.querySelectorAll('.pricing-card, .enterprise-card');
    
    cards.forEach((card, index) => {
        // Adicionar delay de animação escalonado
        card.style.animationDelay = `${index * 0.1}s`;
        
        // Adicionar efeito de entrada
        card.classList.add('animate-in');
    });
}

// Configurar interações dos cards
function setupCardInteractions() {
    const pricingCards = document.querySelectorAll('.pricing-card');
    const enterpriseCard = document.querySelector('.enterprise-card');
    
    // Interações dos cards de preços
    pricingCards.forEach(card => {
        setupCardHoverEffects(card);
        setupCardClickEffects(card);
    });
    
    // Interações do card enterprise
    if (enterpriseCard) {
        setupEnterpriseCardEffects(enterpriseCard);
    }
}

// Efeitos de hover dos cards
function setupCardHoverEffects(card) {
    const planIcon = card.querySelector('.plan-icon');
    const features = card.querySelectorAll('.feature-item');
    const selectBtn = card.querySelector('.select-plan-btn');
    
    card.addEventListener('mouseenter', function() {
        // Efeito de rotação no ícone
        if (planIcon) {
            planIcon.style.transform = 'scale(1.1) rotate(5deg)';
        }
        
        // Animação escalonada das features
        features.forEach((feature, index) => {
            setTimeout(() => {
                feature.style.transform = 'translateX(5px)';
                feature.style.background = 'rgba(224, 32, 32, 0.02)';
            }, index * 50);
        });
        
        // Efeito de pulso no botão
        if (selectBtn) {
            selectBtn.style.transform = 'translateY(-3px) scale(1.02)';
        }
        
        // Adicionar classe de hover
        card.classList.add('card-hovered');
    });
    
    card.addEventListener('mouseleave', function() {
        // Resetar transformações
        if (planIcon) {
            planIcon.style.transform = '';
        }
        
        features.forEach(feature => {
            feature.style.transform = '';
            feature.style.background = '';
        });
        
        if (selectBtn) {
            selectBtn.style.transform = '';
        }
        
        // Remover classe de hover
        card.classList.remove('card-hovered');
    });
}

// Efeitos de clique dos cards
function setupCardClickEffects(card) {
    card.addEventListener('click', function(e) {
        // Não executar se clicou no botão
        if (e.target.closest('.select-plan-btn')) {
            return;
        }
        
        // Efeito de ripple
        createRippleEffect(card, e);
        
        // Destacar card selecionado
        highlightSelectedCard(card);
    });
}

// Criar efeito ripple
function createRippleEffect(element, event) {
    const ripple = document.createElement('div');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${x}px;
        top: ${y}px;
        background: radial-gradient(circle, rgba(224, 32, 32, 0.3) 0%, transparent 70%);
        border-radius: 50%;
        transform: scale(0);
        animation: ripple 0.6s ease-out;
        pointer-events: none;
        z-index: 1;
    `;
    
    element.style.position = 'relative';
    element.appendChild(ripple);
    
    // Remover ripple após animação
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Destacar card selecionado
function highlightSelectedCard(selectedCard) {
    const allCards = document.querySelectorAll('.pricing-card');
    
    // Remover destaque de todos os cards
    allCards.forEach(card => {
        card.classList.remove('selected');
    });
    
    // Adicionar destaque ao card selecionado
    selectedCard.classList.add('selected');
    
    // Efeito de confirmação visual
    showSelectionFeedback(selectedCard);
}

// Mostrar feedback de seleção
function showSelectionFeedback(card) {
    const planName = card.querySelector('.plan-name').textContent;
    
    // Criar notificação temporária
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: linear-gradient(135deg, #28a745, #5cb85c);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
        z-index: 1000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        font-weight: 500;
    `;
    notification.innerHTML = `
        <i class="fas fa-check-circle me-2"></i>
        Plano ${planName} selecionado!
    `;
    
    document.body.appendChild(notification);
    
    // Animar entrada
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remover após 3 segundos
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Configurar efeitos do card enterprise
function setupEnterpriseCardEffects(card) {
    const features = card.querySelectorAll('.enterprise-feature');
    const icon = card.querySelector('.enterprise-icon');
    
    card.addEventListener('mouseenter', function() {
        // Efeito de rotação no ícone
        if (icon) {
            icon.style.transform = 'scale(1.1) rotate(-5deg)';
        }
        
        // Animação das features
        features.forEach((feature, index) => {
            setTimeout(() => {
                feature.style.transform = 'translateX(10px)';
                feature.style.color = '#f39c12';
            }, index * 100);
        });
    });
    
    card.addEventListener('mouseleave', function() {
        if (icon) {
            icon.style.transform = '';
        }
        
        features.forEach(feature => {
            feature.style.transform = '';
            feature.style.color = '';
        });
    });
}

// Configurar seleção de planos
function setupPlanSelection() {
    const selectButtons = document.querySelectorAll('.select-plan-btn');
    const enterpriseBtn = document.querySelector('.enterprise-btn');
    
    selectButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            
            const card = this.closest('.pricing-card');
            const planName = card.querySelector('.plan-name').textContent;
            const planData = card.getAttribute('data-plan');
            
            handlePlanSelection(planData, planName, this);
        });
    });
    
    if (enterpriseBtn) {
        enterpriseBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            handleEnterpriseContact(this);
        });
    }
}

// Lidar com seleção de plano
function handlePlanSelection(planData, planName, button) {
    // Efeito de loading no botão
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processando...';
    button.disabled = true;
    
    // Simular processamento
    setTimeout(() => {
        // Restaurar botão
        button.innerHTML = originalText;
        button.disabled = false;
        
        // Mostrar modal de confirmação ou redirecionar
        showPlanConfirmation(planData, planName);
    }, 1500);
}

// Lidar com contato enterprise
function handleEnterpriseContact(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Conectando...';
    button.disabled = true;
    
    setTimeout(() => {
        button.innerHTML = originalText;
        button.disabled = false;
        
        showEnterpriseModal();
    }, 1000);
}

// Mostrar confirmação de plano
function showPlanConfirmation(planData, planName) {
    const modal = createModal(`
        <div class="modal-header">
            <h4><i class="fas fa-check-circle text-success me-2"></i>Plano Selecionado</h4>
        </div>
        <div class="modal-body">
            <p>Você selecionou o <strong>Plano ${planName}</strong>.</p>
            <p>Deseja prosseguir para finalizar a contratação?</p>
        </div>
        <div class="modal-footer">
            <button class="btn btn-secondary" onclick="closeModal()">Cancelar</button>
            <button class="btn btn-primary" onclick="proceedToCheckout('${planData}')">
                <i class="fas fa-arrow-right me-2"></i>Prosseguir
            </button>
        </div>
    `);
    
    showModal(modal);
}

// Mostrar modal enterprise
function showEnterpriseModal() {
    const modal = createModal(`
        <div class="modal-header">
            <h4><i class="fas fa-rocket me-2"></i>Contato Enterprise</h4>
        </div>
        <div class="modal-body">
            <p>Nossa equipe de especialistas entrará em contato para criar uma solução personalizada para sua instituição.</p>
            <div class="contact-info">
                <div class="contact-item">
                    <i class="fas fa-phone"></i>
                    <span>(11) 9999-9999</span>
                </div>
                <div class="contact-item">
                    <i class="fas fa-envelope"></i>
                    <span>enterprise@hemotec.com</span>
                </div>
                <div class="contact-item">
                    <i class="fas fa-clock"></i>
                    <span>Resposta em até 24h</span>
                </div>
            </div>
        </div>
        <div class="modal-footer">
            <button class="btn btn-secondary" onclick="closeModal()">Fechar</button>
            <button class="btn btn-primary" onclick="openContactForm()">
                <i class="fas fa-comments me-2"></i>Iniciar Conversa
            </button>
        </div>
    `);
    
    showModal(modal);
}

// Criar modal
function createModal(content) {
    const modal = document.createElement('div');
    modal.className = 'custom-modal';
    modal.innerHTML = `
        <div class="modal-overlay" onclick="closeModal()"></div>
        <div class="modal-content">
            ${content}
        </div>
    `;
    
    // Adicionar estilos do modal
    if (!document.getElementById('modal-styles')) {
        const styles = document.createElement('style');
        styles.id = 'modal-styles';
        styles.textContent = `
            .custom-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 10000;
                display: flex;
                align-items: center;
                justify-content: center;
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .modal-overlay {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                backdrop-filter: blur(5px);
            }
            
            .modal-content {
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                max-width: 500px;
                width: 90%;
                max-height: 80vh;
                overflow-y: auto;
                position: relative;
                transform: scale(0.8);
                transition: transform 0.3s ease;
            }
            
            .modal-header {
                padding: 2rem 2rem 1rem;
                border-bottom: 1px solid #eee;
            }
            
            .modal-header h4 {
                margin: 0;
                color: #333;
                font-weight: 600;
            }
            
            .modal-body {
                padding: 2rem;
            }
            
            .modal-footer {
                padding: 1rem 2rem 2rem;
                display: flex;
                gap: 1rem;
                justify-content: flex-end;
            }
            
            .contact-info {
                margin-top: 1.5rem;
            }
            
            .contact-item {
                display: flex;
                align-items: center;
                gap: 1rem;
                padding: 0.8rem 0;
                border-bottom: 1px solid #f0f0f0;
            }
            
            .contact-item:last-child {
                border-bottom: none;
            }
            
            .contact-item i {
                color: #e02020;
                width: 20px;
            }
            
            .btn {
                padding: 0.8rem 1.5rem;
                border: none;
                border-radius: 8px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .btn-primary {
                background: linear-gradient(135deg, #e02020, #ff4040);
                color: white;
            }
            
            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(224, 32, 32, 0.3);
            }
            
            .btn-secondary {
                background: #f8f9fa;
                color: #666;
                border: 1px solid #ddd;
            }
            
            .btn-secondary:hover {
                background: #e9ecef;
            }
        `;
        document.head.appendChild(styles);
    }
    
    return modal;
}

// Mostrar modal
function showModal(modal) {
    document.body.appendChild(modal);
    
    setTimeout(() => {
        modal.style.opacity = '1';
        modal.querySelector('.modal-content').style.transform = 'scale(1)';
    }, 10);
}

// Fechar modal
function closeModal() {
    const modal = document.querySelector('.custom-modal');
    if (modal) {
        modal.style.opacity = '0';
        modal.querySelector('.modal-content').style.transform = 'scale(0.8)';
        
        setTimeout(() => {
            modal.remove();
        }, 300);
    }
}

// Prosseguir para checkout
function proceedToCheckout(planData) {
    closeModal();
    
    // Simular redirecionamento
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        z-index: 10001;
        text-align: center;
    `;
    notification.innerHTML = `
        <i class="fas fa-spinner fa-spin fa-2x text-primary mb-3"></i>
        <h5>Redirecionando para checkout...</h5>
        <p class="text-muted">Aguarde um momento</p>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
        // Aqui você redirecionaria para a página de checkout
        // window.location.href = `/checkout?plan=${planData}`;
        console.log(`Redirecionando para checkout do plano: ${planData}`);
    }, 2000);
}

// Abrir formulário de contato
function openContactForm() {
    closeModal();
    // Aqui você abriria um formulário de contato ou chat
    console.log('Abrindo formulário de contato enterprise');
}

// Configurar animações de scroll
function setupScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-visible');
            }
        });
    }, observerOptions);
    
    // Observar elementos para animação
    const animatedElements = document.querySelectorAll('.pricing-card, .enterprise-card');
    animatedElements.forEach(el => observer.observe(el));
}

// Configurar efeito parallax
function setupParallaxEffect() {
    const heroSection = document.querySelector('.hero-section');
    
    if (heroSection) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            
            heroSection.style.transform = `translateY(${rate}px)`;
        });
    }
}

// Adicionar estilos de animação
const animationStyles = document.createElement('style');
animationStyles.textContent = `
    @keyframes ripple {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
    
    .pricing-card.selected {
        border-color: #e02020 !important;
        box-shadow: 0 15px 50px rgba(224, 32, 32, 0.2) !important;
    }
    
    .animate-visible {
        animation: slideInUp 0.8s ease forwards;
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(animationStyles);

// Tornar funções globais para uso nos modais
window.closeModal = closeModal;
window.proceedToCheckout = proceedToCheckout;
window.openContactForm = openContactForm;

