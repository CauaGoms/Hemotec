document.addEventListener('DOMContentLoaded', function() {
    // Dados das campanhas (simulando dados que viriam do backend)
    const campaignsData = {
        'junho-vermelho': {
            title: 'Junho Vermelho 2025',
            subtitle: 'Mês Nacional do Doador de Sangue - Participe da maior campanha de doação do ano!',
            status: 'Campanha Ativa',
            statusClass: 'status-active',
            currentDonations: 1847,
            targetDonations: 2500,
            daysRemaining: 15,
            heroImage: 'https://images.unsplash.com/photo-1615461066841-6116e61058f4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80',
            description: `
                <p>O Junho Vermelho é uma campanha nacional que visa conscientizar a população sobre a importância da doação de sangue. Durante todo o mês de junho, mobilizamos doadores de todo o país para atingir nossa meta de 2.500 doações.</p>
                <p>Esta campanha é especialmente importante porque coincide com o período de inverno, quando tradicionalmente há uma queda nas doações de sangue. Seu apoio é fundamental para mantermos os estoques dos hemocentros em níveis adequados.</p>
                <h4>Objetivos da Campanha:</h4>
                <ul>
                    <li>Aumentar o estoque de sangue em 30% durante o mês de junho</li>
                    <li>Conscientizar sobre a importância da doação regular</li>
                    <li>Recrutar novos doadores de primeira viagem</li>
                    <li>Fortalecer a cultura de solidariedade na comunidade</li>
                </ul>
            `
        },
        'doacao-empresarial': {
            title: 'Doação Coletiva Empresarial',
            subtitle: 'Empresas se unem para promover a doação de sangue entre seus colaboradores.',
            status: 'Campanha Ativa',
            statusClass: 'status-active',
            currentDonations: 650,
            targetDonations: 1000,
            daysRemaining: 45,
            heroImage: 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?auto=format&fit=crop&w=1470&q=80',
            description: `
                <p>A campanha Doação Coletiva Empresarial é uma iniciativa que une empresas parceiras para promover a cultura de doação de sangue no ambiente corporativo.</p>
                <p>Através de parcerias estratégicas, facilitamos o processo de doação para colaboradores, oferecendo horários flexíveis e postos de coleta nas próprias empresas.</p>
                <h4>Benefícios para as Empresas:</h4>
                <ul>
                    <li>Fortalecimento da responsabilidade social corporativa</li>
                    <li>Engajamento dos colaboradores em causas sociais</li>
                    <li>Melhoria do clima organizacional</li>
                    <li>Reconhecimento como empresa socialmente responsável</li>
                </ul>
            `
        },
        'volta-aulas': {
            title: 'Volta às Aulas Solidária',
            subtitle: 'Campanha direcionada para estudantes e professores promovendo a cultura de doação.',
            status: 'Próxima Campanha',
            statusClass: 'status-upcoming',
            currentDonations: 0,
            targetDonations: 800,
            daysRemaining: 60,
            heroImage: 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?auto=format&fit=crop&w=1470&q=80',
            description: `
                <p>A campanha Volta às Aulas Solidária tem como objetivo introduzir a cultura de doação de sangue no ambiente educacional, envolvendo estudantes, professores e funcionários.</p>
                <p>Realizamos palestras educativas, ações de conscientização e facilitamos o processo de doação dentro das instituições de ensino.</p>
                <h4>Ações Planejadas:</h4>
                <ul>
                    <li>Palestras sobre a importância da doação de sangue</li>
                    <li>Postos de coleta móveis nas universidades</li>
                    <li>Campanhas de conscientização nas redes sociais</li>
                    <li>Parcerias com grêmios estudantis e centros acadêmicos</li>
                </ul>
            `
        }
    };

    // Elementos do DOM
    const campaignHero = document.getElementById('campaignHero');
    const campaignTitle = document.getElementById('campaignTitle');
    const campaignSubtitle = document.getElementById('campaignSubtitle');
    const campaignBadge = document.getElementById('campaignBadge');
    const campaignStatus = document.getElementById('campaignStatus');
    const currentDonations = document.getElementById('currentDonations');
    const targetDonations = document.getElementById('targetDonations');
    const daysRemaining = document.getElementById('daysRemaining');
    const progressFill = document.getElementById('progressFill');
    const campaignDescription = document.getElementById('campaignDescription');
    const shareBtn = document.getElementById('shareBtn');
    const shareModal = new bootstrap.Modal(document.getElementById('shareModal'));

    // Carrossel de depoimentos
    const testimonialItems = document.querySelectorAll('.testimonial-item');
    const testimonialBtns = document.querySelectorAll('.testimonial-btn');
    let currentTestimonial = 0;

    // Função para obter o ID da campanha da URL
    function getCampaignIdFromUrl() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('id') || 'junho-vermelho';
    }

    // Função para carregar dados da campanha
    function loadCampaignData(campaignId) {
        const campaign = campaignsData[campaignId];
        if (!campaign) {
            console.error('Campanha não encontrada:', campaignId);
            return;
        }

        // Atualizar elementos da página
        campaignTitle.textContent = campaign.title;
        campaignSubtitle.textContent = campaign.subtitle;
        campaignStatus.textContent = campaign.status;
        campaignBadge.className = `campaign-badge ${campaign.statusClass}`;
        
        // Atualizar estatísticas
        animateNumber(currentDonations, campaign.currentDonations);
        animateNumber(targetDonations, campaign.targetDonations);
        animateNumber(daysRemaining, campaign.daysRemaining);
        
        // Atualizar barra de progresso
        const progressPercentage = Math.round((campaign.currentDonations / campaign.targetDonations) * 100);
        document.getElementById('progressPercentage').textContent = progressPercentage + '%';
        progressFill.style.width = progressPercentage + '%';
        
        // Atualizar imagem de fundo do hero
        campaignHero.style.backgroundImage = `linear-gradient(135deg, rgba(224, 32, 32, 0.9), rgba(192, 16, 16, 0.8)), url('${campaign.heroImage}')`;
        
        // Atualizar descrição
        campaignDescription.innerHTML = campaign.description;
        
        // Atualizar estatísticas da sidebar
        updateSidebarStats(campaign);
        
        // Atualizar URL sem recarregar a página
        const newUrl = `${window.location.pathname}?id=${campaignId}`;
        window.history.pushState({campaignId}, '', newUrl);
    }

    // Função para animar números
    function animateNumber(element, targetValue) {
        const startValue = 0;
        const duration = 2000;
        const startTime = performance.now();
        
        function updateNumber(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function (ease-out)
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const currentValue = Math.round(startValue + (targetValue - startValue) * easeOut);
            
            element.textContent = currentValue.toLocaleString('pt-BR');
            
            if (progress < 1) {
                requestAnimationFrame(updateNumber);
            }
        }
        
        requestAnimationFrame(updateNumber);
    }

    // Função para atualizar estatísticas da sidebar
    function updateSidebarStats(campaign) {
        const totalParticipants = document.getElementById('totalParticipants');
        const newDonors = document.getElementById('newDonors');
        const recurringDonors = document.getElementById('recurringDonors');
        const livesImpacted = document.getElementById('livesImpacted');
        
        if (totalParticipants) animateNumber(totalParticipants, campaign.currentDonations);
        if (newDonors) animateNumber(newDonors, Math.round(campaign.currentDonations * 0.23));
        if (recurringDonors) animateNumber(recurringDonors, Math.round(campaign.currentDonations * 0.77));
        if (livesImpacted) animateNumber(livesImpacted, campaign.currentDonations * 4);
    }

    // Função para o carrossel de depoimentos
    function showTestimonial(index) {
        testimonialItems.forEach((item, i) => {
            item.classList.toggle('active', i === index);
        });
        
        testimonialBtns.forEach((btn, i) => {
            btn.classList.toggle('active', i === index);
        });
        
        currentTestimonial = index;
    }

    // Auto-play do carrossel de depoimentos
    function autoPlayTestimonials() {
        setInterval(() => {
            currentTestimonial = (currentTestimonial + 1) % testimonialItems.length;
            showTestimonial(currentTestimonial);
        }, 5000);
    }

    // Event listeners para os botões do carrossel
    testimonialBtns.forEach((btn, index) => {
        btn.addEventListener('click', () => {
            showTestimonial(index);
        });
    });

    // Função de compartilhamento
    function shareContent(platform) {
        const campaignId = getCampaignIdFromUrl();
        const campaign = campaignsData[campaignId];
        const url = window.location.href;
        const text = `Participe da campanha "${campaign.title}" e ajude a salvar vidas! 🩸❤️`;
        
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

    // Event listeners para compartilhamento
    shareBtn.addEventListener('click', () => {
        shareModal.show();
        document.getElementById('shareLink').value = window.location.href;
    });

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

    // Função para copiar link
    function copyToClipboard() {
        const shareLink = document.getElementById('shareLink');
        shareLink.select();
        shareLink.setSelectionRange(0, 99999);
        
        try {
            document.execCommand('copy');
            showToast('Link copiado para a área de transferência!', 'success');
        } catch (err) {
            showToast('Erro ao copiar link', 'error');
        }
    }

    // Event listener para o botão de copiar
    document.getElementById('copyLinkBtn').addEventListener('click', copyToClipboard);

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

    // Função para navegação entre campanhas
    function setupCampaignNavigation() {
        // Adicionar event listeners para links de campanhas relacionadas
        document.querySelectorAll('.related-campaign-item').forEach((item, index) => {
            item.addEventListener('click', () => {
                const campaignIds = ['doacao-empresarial', 'volta-aulas', 'junho-vermelho'];
                const campaignId = campaignIds[index];
                if (campaignId && campaignsData[campaignId]) {
                    loadCampaignData(campaignId);
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                }
            });
        });

        // Adicionar event listeners para botões "Saiba Mais" na página de campanhas
        document.querySelectorAll('.btn-campaign').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const campaignCard = btn.closest('.campaign-item');
                if (campaignCard) {
                    const title = campaignCard.getAttribute('data-title');
                    let campaignId = 'junho-vermelho'; // default
                    
                    if (title.includes('empresarial')) campaignId = 'doacao-empresarial';
                    else if (title.includes('aulas')) campaignId = 'volta-aulas';
                    
                    // Navegar para a página de detalhes
                    window.location.href = `/doador/campanha/detalhes?id=${campaignId}`;
                }
            });
        });
    }

    // Função para animações de entrada
    function setupScrollAnimations() {
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

    // Função para atualizar estatísticas em tempo real (simulação)
    function simulateRealTimeUpdates() {
        setInterval(() => {
            const campaignId = getCampaignIdFromUrl();
            const campaign = campaignsData[campaignId];
            
            if (campaign && campaign.status === 'Campanha Ativa') {
                // Simular pequenos incrementos nas doações
                const increment = Math.random() < 0.3 ? 1 : 0; // 30% de chance de incremento
                if (increment && campaign.currentDonations < campaign.targetDonations) {
                    campaign.currentDonations += increment;
                    
                    // Atualizar elementos na página
                    currentDonations.textContent = campaign.currentDonations.toLocaleString('pt-BR');
                    
                    const progressPercentage = Math.round((campaign.currentDonations / campaign.targetDonations) * 100);
                    document.getElementById('progressPercentage').textContent = progressPercentage + '%';
                    progressFill.style.width = progressPercentage + '%';
                    
                    // Atualizar sidebar
                    const totalParticipants = document.getElementById('totalParticipants');
                    const livesImpacted = document.getElementById('livesImpacted');
                    if (totalParticipants) totalParticipants.textContent = campaign.currentDonations.toLocaleString('pt-BR');
                    if (livesImpacted) livesImpacted.textContent = (campaign.currentDonations * 4).toLocaleString('pt-BR');
                }
            }
        }, 30000); // Atualizar a cada 30 segundos
    }

    // Função para gerenciar o histórico do navegador
    window.addEventListener('popstate', (event) => {
        if (event.state && event.state.campaignId) {
            loadCampaignData(event.state.campaignId);
        }
    });

    // Função para adicionar efeitos hover nos cards de localização
    function setupLocationCardEffects() {
        document.querySelectorAll('.location-card').forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px) scale(1.02)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });
    }

    // Inicialização
    function init() {
        const campaignId = getCampaignIdFromUrl();
        loadCampaignData(campaignId);
        autoPlayTestimonials();
        setupCampaignNavigation();
        setupScrollAnimations();
        setupLocationCardEffects();
        simulateRealTimeUpdates();
        
        // Adicionar classe para animações CSS
        document.body.classList.add('page-loaded');
        
        console.log('Página de detalhes da campanha carregada com sucesso!');
    }

    // Executar inicialização
    init();

    // Adicionar suporte para navegação por teclado
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
            const direction = e.key === 'ArrowLeft' ? -1 : 1;
            const newIndex = (currentTestimonial + direction + testimonialItems.length) % testimonialItems.length;
            showTestimonial(newIndex);
        }
    });

    // Adicionar funcionalidade de busca rápida
    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.placeholder = 'Buscar informações na página...';
    searchInput.style.cssText = `
        position: fixed;
        top: 10px;
        right: 10px;
        padding: 0.5rem;
        border: 2px solid var(--hemotec-red);
        border-radius: 20px;
        display: none;
        z-index: 9999;
    `;
    document.body.appendChild(searchInput);

    // Ativar busca com Ctrl+F
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'f') {
            e.preventDefault();
            searchInput.style.display = searchInput.style.display === 'none' ? 'block' : 'none';
            if (searchInput.style.display === 'block') {
                searchInput.focus();
            }
        }
    });

    // Funcionalidade de busca
    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const textElements = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, span, li');
        
        textElements.forEach(el => {
            if (el.textContent.toLowerCase().includes(searchTerm) && searchTerm.length > 2) {
                el.style.backgroundColor = 'yellow';
            } else {
                el.style.backgroundColor = '';
            }
        });
    });
});