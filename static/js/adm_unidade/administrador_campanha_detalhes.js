document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funcionalidades de compartilhamento
    initSharingFeatures();

    // Inicializar animações
    initScrollAnimations();

    // Inicializar efeitos hover
    initHoverEffects();

    // Inicializar exclusão
    initDeleteFunctionality();

    // Função para inicializar funcionalidades de compartilhamento
    function initSharingFeatures() {
        // Event listeners para botões de compartilhamento
        document.querySelectorAll('[data-platform]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const platform = e.currentTarget.getAttribute('data-platform');
                if (platform === 'link') {
                    copyToClipboard();
                } else {
                    shareContent(platform);
                }
            });
        });
    }

    // Função de compartilhamento
    function shareContent(platform) {
        const url = window.location.href;
        const title = document.querySelector('.campaign-title-modern').textContent;
        const text = `Confira a campanha "${title}" no Hemotec! 🩸❤️`;
        
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
        const url = window.location.href;
        
        // Usar a API moderna de clipboard
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(url).then(() => {
                showToast('Link copiado para a área de transferência!', 'success');
            }).catch(err => {
                console.error('Erro ao copiar:', err);
                showToast('Erro ao copiar link', 'error');
            });
        } else {
            // Fallback para navegadores antigos
            const textarea = document.createElement('textarea');
            textarea.value = url;
            textarea.style.position = 'fixed';
            textarea.style.opacity = '0';
            document.body.appendChild(textarea);
            textarea.select();
            
            try {
                document.execCommand('copy');
                showToast('Link copiado para a área de transferência!', 'success');
            } catch (err) {
                showToast('Erro ao copiar link', 'error');
            }
            
            document.body.removeChild(textarea);
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
        document.querySelectorAll('.campaign-section').forEach(el => {
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

        // Efeitos nas campanhas relacionadas
        document.querySelectorAll('.related-campaign').forEach(item => {
            item.addEventListener('mouseenter', function() {
                this.style.transform = 'translateX(5px) scale(1.02)';
            });
            
            item.addEventListener('mouseleave', function() {
                this.style.transform = 'translateX(0) scale(1)';
            });
        });
    }

    // Função para confirmar exclusão
    function initDeleteFunctionality() {
        const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
        
        if (confirmDeleteBtn) {
            confirmDeleteBtn.addEventListener('click', async () => {
                const urlParts = window.location.pathname.split('/');
                const campanhaId = urlParts[urlParts.length - 1];

                if (!campanhaId) return;

                try {
                    const response = await fetch(`/administrador/campanha/excluir/${campanhaId}`, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });

                    if (response.ok) {
                        // Fechar modal
                        const modal = bootstrap.Modal.getInstance(document.getElementById('deleteModal'));
                        modal.hide();

                        // Mostrar mensagem de sucesso
                        showToast('Campanha excluída com sucesso!', 'success');

                        // Redirecionar para lista após 1 segundo
                        setTimeout(() => {
                            window.location.href = '/administrador/campanha';
                        }, 1000);
                    } else {
                        showToast('Erro ao excluir campanha', 'error');
                    }
                } catch (error) {
                    console.error('Erro:', error);
                    showToast('Erro ao excluir campanha', 'error');
                }
            });
        }
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

    // Adicionar classe para indicar que a página foi carregada
    document.body.classList.add('page-loaded');
    
    console.log('Página de detalhes da campanha carregada com sucesso!');
});

// Função global para confirmar exclusão (chamada do HTML)
function confirmarExclusao(campanhaId) {
    const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
    modal.show();
}
