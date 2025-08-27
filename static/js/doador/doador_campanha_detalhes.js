document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const shareBtn = document.getElementById('shareBtn');
    const shareModal = new bootstrap.Modal(document.getElementById('shareModal'));
    const copyLinkBtn = document.getElementById('copyLinkBtn');
    const shareLink = document.getElementById('shareLink');

    // Carrossel de depoimentos
    const testimonialItems = document.querySelectorAll('.testimonial-item');
    const testimonialBtns = document.querySelectorAll('.testimonial-btn');
    let currentTestimonial = 0;

    // Inicializar carrossel de depoimentos se existir
    if (testimonialItems.length > 0) {
        initTestimonialCarousel();
    }

    // Inicializar funcionalidades de compartilhamento
    initSharingFeatures();

    // Inicializar animações
    initScrollAnimations();

    // Inicializar efeitos hover
    initHoverEffects();

    // Função para o carrossel de depoimentos
    function initTestimonialCarousel() {
        // Mostrar depoimento específico
        function showTestimonial(index) {
            testimonialItems.forEach((item, i) => {
                item.classList.toggle('active', i === index);
            });
            
            testimonialBtns.forEach((btn, i) => {
                btn.classList.toggle('active', i === index);
            });
            
            currentTestimonial = index;
        }

        // Event listeners para os botões do carrossel
        testimonialBtns.forEach((btn, index) => {
            btn.addEventListener('click', () => {
                showTestimonial(index);
            });
        });

        // Auto-play do carrossel
        setInterval(() => {
            currentTestimonial = (currentTestimonial + 1) % testimonialItems.length;
            showTestimonial(currentTestimonial);
        }, 5000);

        // Navegação por teclado
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
                const direction = e.key === 'ArrowLeft' ? -1 : 1;
                const newIndex = (currentTestimonial + direction + testimonialItems.length) % testimonialItems.length;
                showTestimonial(newIndex);
            }
        });
    }

    // Função para inicializar funcionalidades de compartilhamento
    function initSharingFeatures() {
        // Abrir modal de compartilhamento
        if (shareBtn) {
            shareBtn.addEventListener('click', () => {
                shareModal.show();
                shareLink.value = window.location.href;
            });
        }

        // Event listeners para botões de compartilhamento
        document.querySelectorAll('[data-platform]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const platform = e.currentTarget.getAttribute('data-platform');
                if (platform === 'copy') {
                    copyToClipboard();
                } else {
                    shareContent(platform);
                }
            });
        });

        // Copiar link
        if (copyLinkBtn) {
            copyLinkBtn.addEventListener('click', copyToClipboard);
        }
    }

    // Função de compartilhamento
    function shareContent(platform) {
        const url = window.location.href;
        const title = document.querySelector('.campaign-title').textContent;
        const text = `Participe da campanha "${title}" e ajude a salvar vidas! 🩸❤️`;
        
        const shareUrls = {
            facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`,
            twitter: `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`,
            whatsapp: `https://wa.me/?text=${encodeURIComponent(text + ' ' + url)}`,
            linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`
        };
        
        if (shareUrls[platform]) {
            window.open(shareUrls[platform], '_blank', 'width=600,height=400');
        }
    }

    // Função para copiar link
    function copyToClipboard() {
        shareLink.select();
        shareLink.setSelectionRange(0, 99999);
        
        try {
            document.execCommand('copy');
            showToast('Link copiado para a área de transferência!', 'success');
        } catch (err) {
            showToast('Erro ao copiar link', 'error');
        }
    }

    // Função para mostrar toast
    function showToast(message, type = 'info') {
        // Remove toasts existentes
        const existingToasts = document.querySelectorAll('.toast-notification');
        existingToasts.forEach(toast => toast.remove());

        // Cria novo toast
        const toast = document.createElement('div');
        toast.className = `toast-notification toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'} me-2"></i>
                ${message}
            </div>
        `;

        // Adiciona estilos
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#28a745' : '#dc3545'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            z-index: 9999;
            animation: slideInRight 0.3s ease-out;
        `;

        document.body.appendChild(toast);

        // Remove após 3 segundos
        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // Função para animações de entrada
    function initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        // Observar elementos que devem animar
        document.querySelectorAll('.content-section, .sidebar-card').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'all 0.6s ease-out';
            observer.observe(el);
        });
    }

    // Função para efeitos hover
    function initHoverEffects() {
        // Efeitos nos cards de localização
        document.querySelectorAll('.location-card').forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px) scale(1.02)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });

        // Efeitos nos cards de reconhecimento
        document.querySelectorAll('.recognition-item').forEach(item => {
            item.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-3px) scale(1.02)';
            });
            
            item.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });

        // Efeitos nas campanhas relacionadas
        document.querySelectorAll('.related-campaign-item').forEach(item => {
            item.addEventListener('mouseenter', function() {
                this.style.transform = 'translateX(5px) scale(1.02)';
            });
            
            item.addEventListener('mouseleave', function() {
                this.style.transform = 'translateX(0) scale(1)';
            });
        });
    }

    // Adicionar estilos CSS para as animações do toast
    const toastStyles = document.createElement('style');
    toastStyles.textContent = `
        @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOutRight {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
        .toast-content {
            display: flex;
            align-items: center;
            font-weight: 500;
        }
    `;
    document.head.appendChild(toastStyles);

    // Animação da barra de progresso
    function animateProgressBar() {
        const progressFill = document.querySelector('.progress-fill');
        if (progressFill) {
            const targetProgress = progressFill.getAttribute('data-progress') || 0;
            const targetWidth = targetProgress + '%';
            progressFill.style.width = '0%';
            
            setTimeout(() => {
                progressFill.style.transition = 'width 2s ease-out';
                progressFill.style.width = targetWidth;
            }, 500);
        }
    }

    // Animação dos números das estatísticas
    function animateNumbers() {
        const numberElements = document.querySelectorAll('.stat-number, .stat-value');
        
        numberElements.forEach(element => {
            const text = element.textContent;
            const number = parseInt(text.replace(/\D/g, ''));
            
            if (number && number > 0) {
                animateNumber(element, number, text);
            }
        });
    }

    function animateNumber(element, targetValue, originalText) {
        const startValue = 0;
        const duration = 2000;
        const startTime = performance.now();
        
        function updateNumber(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function (ease-out)
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const currentValue = Math.round(startValue + (targetValue - startValue) * easeOut);
            
            // Manter formato original (com % ou outros caracteres)
            if (originalText.includes('%')) {
                element.textContent = currentValue + '%';
            } else if (originalText.includes('.')) {
                element.textContent = currentValue.toLocaleString('pt-BR');
            } else {
                element.textContent = currentValue.toLocaleString('pt-BR');
            }
            
            if (progress < 1) {
                requestAnimationFrame(updateNumber);
            }
        }
        
        requestAnimationFrame(updateNumber);
    }

    // Inicializar animações após carregamento
    setTimeout(() => {
        animateProgressBar();
        animateNumbers();
    }, 1000);

    // Adicionar classe para indicar que a página foi carregada
    document.body.classList.add('page-loaded');
    
    console.log('Página de detalhes da campanha carregada com sucesso!');
});

