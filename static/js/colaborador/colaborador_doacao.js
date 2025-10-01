// Gestão de Doações - Colaborador - JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const searchInput = document.getElementById('searchInput');
    const donationsList = document.getElementById('donationsList');
    const noDonationsMessage = document.getElementById('noDonationsMessage');
    const filterButtons = document.querySelectorAll('.filter-btn-modern');
    const detailsModal = new bootstrap.Modal(document.getElementById('detailsModal'));
    const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
    
    // Estado da aplicação
    let currentFilter = 'all';
    let currentSearch = '';
    let donations = [];
    
    // Dados simulados das doações
    const mockDonations = [
        {
            id: 1,
            doador: {
                nome: 'João Silva',
                cpf: '123.456.789-00',
                telefone: '(28) 99999-9999',
                idade: 25,
                tipoSanguineo: 'O+',
                cidade: 'Cachoeiro de Itapemirim, ES',
                primeiraDoacao: true
            },
            status: 'aguardando_triagem',
            dataAgendamento: '2025-01-15T09:00:00',
            observacoes: 'Primeira doação do doador'
        },
        {
            id: 2,
            doador: {
                nome: 'Maria Santos',
                cpf: '987.654.321-00',
                telefone: '(28) 98888-8888',
                idade: 32,
                tipoSanguineo: 'A-',
                cidade: 'Cachoeiro de Itapemirim, ES',
                peso: 65,
                altura: 168
            },
            status: 'aguardando_doacao',
            dataTriagem: '2025-01-14T14:30:00',
            triagemAprovada: true,
            observacoes: 'Triagem aprovada sem restrições'
        },
        {
            id: 3,
            doador: {
                nome: 'Carlos Oliveira',
                cpf: '456.789.123-00',
                telefone: '(28) 97777-7777',
                idade: 28,
                tipoSanguineo: 'B+',
                cidade: 'Cachoeiro de Itapemirim, ES'
            },
            status: 'aguardando_exames',
            dataDoacao: '2025-01-13T10:15:00',
            volumeColetado: 450,
            medicoResponsavel: 'Dr. João Mendes',
            observacoes: 'Doação realizada sem intercorrências'
        },
        {
            id: 4,
            doador: {
                nome: 'Ana Costa',
                cpf: '789.123.456-00',
                telefone: '(28) 96666-6666',
                idade: 35,
                tipoSanguineo: 'AB+',
                cidade: 'Cachoeiro de Itapemirim, ES'
            },
            status: 'concluida',
            dataConclusao: '2025-01-12T16:45:00',
            examesAprovados: true,
            estoqueAtualizado: true,
            observacoes: 'Processo concluído com sucesso'
        },
        {
            id: 5,
            doador: {
                nome: 'Pedro Almeida',
                cpf: '321.654.987-00',
                telefone: '(28) 95555-5555',
                idade: 29,
                tipoSanguineo: 'O-',
                cidade: 'Cachoeiro de Itapemirim, ES'
            },
            status: 'aguardando_triagem',
            dataAgendamento: '2025-01-16T14:00:00',
            observacoes: 'Doador regular - última doação há 4 meses'
        },
        {
            id: 6,
            doador: {
                nome: 'Lucia Ferreira',
                cpf: '654.321.789-00',
                telefone: '(28) 94444-4444',
                idade: 27,
                tipoSanguineo: 'A+',
                cidade: 'Cachoeiro de Itapemirim, ES'
            },
            status: 'aguardando_doacao',
            dataTriagem: '2025-01-15T11:00:00',
            triagemAprovada: true,
            observacoes: 'Apta para doação'
        }
    ];
    
    // Inicialização
    init();
    
    function init() {
        donations = [...mockDonations];
        setupEventListeners();
        renderDonations();
    }
    
    // Configurar Event Listeners
    function setupEventListeners() {
        // Busca
        searchInput.addEventListener('input', debounce(handleSearch, 300));
        
        // Filtros
        filterButtons.forEach(button => {
            button.addEventListener('click', handleFilter);
        });
        
        // Limpar busca
        const clearSearchBtn = document.getElementById('clearSearch');
        if (clearSearchBtn) {
            clearSearchBtn.addEventListener('click', () => {
                searchInput.value = '';
                currentSearch = '';
                renderDonations();
            });
        }
        
        // Ações dos cards
        setupCardActions();
    }
    
    function setupCardActions() {
        // Event delegation para botões dinâmicos
        donationsList.addEventListener('click', function(e) {
            const button = e.target.closest('button');
            if (!button) return;
            
            const action = button.getAttribute('onclick');
            if (action) {
                // Prevenir execução do onclick inline
                e.preventDefault();
                
                // Extrair ID e função
                const match = action.match(/(\\w+)\\('(\\d+)'\\)/);
                if (match) {
                    const [, functionName, id] = match;
                    
                    // Executar função correspondente
                    switch (functionName) {
                        case 'fazerTriagem':
                            fazerTriagem(id);
                            break;
                        case 'inserirDoacao':
                            inserirDoacao(id);
                            break;
                        case 'inserirExame':
                            inserirExame(id);
                            break;
                        case 'gerarComprovante':
                            gerarComprovante(id);
                            break;
                        case 'verDetalhes':
                            verDetalhes(id);
                            break;
                        case 'verTriagem':
                            verTriagem(id);
                            break;
                        case 'verDoacao':
                            verDoacao(id);
                            break;
                        case 'verHistorico':
                            verHistorico(id);
                            break;
                    }
                }
            }
        });
    }
    
    // Busca
    function handleSearch(event) {
        currentSearch = event.target.value.toLowerCase().trim();
        renderDonations();
    }
    
    // Filtros
    function handleFilter(event) {
        event.preventDefault();
        
        const status = event.target.closest('.filter-btn-modern').getAttribute('data-status');
        if (!status) return;
        
        currentFilter = status;
        
        // Atualizar botões ativos
        filterButtons.forEach(btn => btn.classList.remove('active'));
        event.target.closest('.filter-btn-modern').classList.add('active');
        
        renderDonations();
    }
    
    // Renderizar doações
    function renderDonations() {
        const filteredDonations = filterDonations();
        
        if (filteredDonations.length === 0) {
            donationsList.style.display = 'none';
            noDonationsMessage.style.display = 'block';
            return;
        }
        
        donationsList.style.display = 'flex';
        noDonationsMessage.style.display = 'none';
        
        donationsList.innerHTML = filteredDonations.map(donation => createDonationCard(donation)).join('');
    }
    
    // Filtrar doações
    function filterDonations() {
        return donations.filter(donation => {
            // Filtro por status
            const statusMatch = currentFilter === 'all' || donation.status === currentFilter;
            
            // Filtro por busca
            const searchMatch = !currentSearch || 
                donation.doador.nome.toLowerCase().includes(currentSearch) ||
                donation.doador.cpf.includes(currentSearch) ||
                donation.doador.telefone.includes(currentSearch);
            
            return statusMatch && searchMatch;
        });
    }
    
    // Criar card de doação
    function createDonationCard(donation) {
        const statusConfig = getStatusConfig(donation.status);
        const donorInfo = createDonorInfo(donation);
        const details = createDonationDetails(donation);
        const actions = createDonationActions(donation);
        
        return `
            <div class="donation-card ${donation.status}" data-status="${donation.status}" data-donor="${donation.doador.nome}">
                <div class="card-header">
                    <div class="donor-info">
                        <div class="donor-avatar">
                            <i class="fas fa-user"></i>
                        </div>
                        <div class="donor-details">
                            <h4 class="donor-name">${donation.doador.nome}</h4>
                            <p class="donor-info-text">
                                ${donorInfo}
                            </p>
                        </div>
                    </div>
                    <div class="status-badge ${statusConfig.class}">
                        <i class="${statusConfig.icon}"></i>
                        ${statusConfig.text}
                    </div>
                </div>
                <div class="card-body">
                    <div class="donation-details">
                        ${details}
                    </div>
                    <div class="card-actions">
                        ${actions}
                    </div>
                </div>
            </div>
        `;
    }
    
    // Configuração de status
    function getStatusConfig(status) {
        const configs = {
            aguardando_triagem: {
                class: 'triagem',
                icon: 'fas fa-clipboard-check',
                text: 'Aguardando Triagem'
            },
            aguardando_doacao: {
                class: 'doacao',
                icon: 'fas fa-hand-holding-heart',
                text: 'Aguardando Coleta'
            },
            aguardando_exames: {
                class: 'exames',
                icon: 'fas fa-vial',
                text: 'Aguardando Exames'
            },
            concluida: {
                class: 'concluida',
                icon: 'fas fa-check-circle',
                text: 'Concluída'
            }
        };
        
        return configs[status] || configs.aguardando_triagem;
    }
    
    // Criar informações do doador
    function createDonorInfo(donation) {
        const info = [
            `<span><i class="fas fa-id-card"></i> CPF: ${donation.doador.cpf}</span>`,
            `<span><i class="fas fa-tint"></i> Tipo: ${donation.doador.tipoSanguineo}</span>`
        ];
        
        if (donation.dataAgendamento) {
            info.push(`<span><i class="fas fa-calendar"></i> Agendado: ${formatDateTime(donation.dataAgendamento)}</span>`);
        } else if (donation.dataTriagem) {
            info.push(`<span><i class="fas fa-calendar"></i> Triagem: ${formatDateTime(donation.dataTriagem)}</span>`);
        } else if (donation.dataDoacao) {
            info.push(`<span><i class="fas fa-calendar"></i> Doação: ${formatDateTime(donation.dataDoacao)}</span>`);
        } else if (donation.dataConclusao) {
            info.push(`<span><i class="fas fa-calendar"></i> Concluída: ${formatDateTime(donation.dataConclusao)}</span>`);
        }
        
        return info.join('');
    }
    
    // Criar detalhes da doação
    function createDonationDetails(donation) {
        const details = [
            `<div class="detail-item">
                <i class="fas fa-phone"></i>
                <span>${donation.doador.telefone}</span>
            </div>`,
            `<div class="detail-item">
                <i class="fas fa-birthday-cake"></i>
                <span>${donation.doador.idade} anos</span>
            </div>`
        ];
        
        switch (donation.status) {
            case 'aguardando_triagem':
                details.push(`<div class="detail-item">
                    <i class="fas fa-map-marker-alt"></i>
                    <span>${donation.doador.cidade}</span>
                </div>`);
                details.push(`<div class="detail-item">
                    <i class="fas fa-clock"></i>
                    <span>${donation.doador.primeiraDoacao ? 'Primeira doação' : 'Doador regular'}</span>
                </div>`);
                break;
                
            case 'aguardando_doacao':
                details.push(`<div class="detail-item">
                    <i class="fas fa-check-circle text-success"></i>
                    <span>Triagem aprovada</span>
                </div>`);
                if (donation.doador.peso && donation.doador.altura) {
                    details.push(`<div class="detail-item">
                        <i class="fas fa-weight"></i>
                        <span>${donation.doador.peso}kg - ${donation.doador.altura}cm</span>
                    </div>`);
                }
                break;
                
            case 'aguardando_exames':
                details.push(`<div class="detail-item">
                    <i class="fas fa-flask"></i>
                    <span>${donation.volumeColetado}ml coletados</span>
                </div>`);
                details.push(`<div class="detail-item">
                    <i class="fas fa-user-md"></i>
                    <span>${donation.medicoResponsavel}</span>
                </div>`);
                break;
                
            case 'concluida':
                details.push(`<div class="detail-item">
                    <i class="fas fa-check-circle text-success"></i>
                    <span>Exames aprovados</span>
                </div>`);
                details.push(`<div class="detail-item">
                    <i class="fas fa-box"></i>
                    <span>Estoque atualizado</span>
                </div>`);
                break;
        }
        
        return details.join('');
    }
    
    // Criar ações da doação
    function createDonationActions(donation) {
        const actions = [];
        
        switch (donation.status) {
            case 'aguardando_triagem':
                actions.push(`<button class="btn btn-primary action-btn" onclick="fazerTriagem('${donation.id}')">
                    <i class="fas fa-clipboard-check"></i>
                    Fazer Triagem
                </button>`);
                actions.push(`<button class="btn btn-outline-secondary" onclick="verDetalhes('${donation.id}')">
                    <i class="fas fa-eye"></i>
                    Ver Detalhes
                </button>`);
                break;
                
            case 'aguardando_doacao':
                actions.push(`<button class="btn btn-success action-btn" onclick="inserirDoacao('${donation.id}')">
                    <i class="fas fa-tint"></i>
                    Inserir Coleta
                </button>`);
                actions.push(`<button class="btn btn-outline-secondary" onclick="verTriagem('${donation.id}')">
                    <i class="fas fa-clipboard-list"></i>
                    Ver Triagem
                </button>`);
                break;
                
            case 'aguardando_exames':
                actions.push(`<button class="btn btn-warning action-btn" onclick="inserirExame('${donation.id}')">
                    <i class="fas fa-vial"></i>
                    Inserir Exame
                </button>`);
                actions.push(`<button class="btn btn-outline-secondary" onclick="verDoacao('${donation.id}')">
                    <i class="fas fa-tint"></i>
                    Ver Doação
                </button>`);
                break;
                
            case 'concluida':
                actions.push(`<button class="btn btn-info action-btn" onclick="gerarComprovante('${donation.id}')">
                    <i class="fas fa-certificate"></i>
                    Gerar Comprovante
                </button>`);
                actions.push(`<button class="btn btn-outline-secondary" onclick="verHistorico('${donation.id}')">
                    <i class="fas fa-history"></i>
                    Ver Histórico
                </button>`);
                break;
        }
        
        return actions.join('');
    }
    
    // Ações específicas
    function fazerTriagem(id) {
        const donation = donations.find(d => d.id == id);
        if (!donation) return;
        
        showConfirmModal(
            'Iniciar Triagem',
            `Deseja iniciar a triagem para o doador <strong>${donation.doador.nome}</strong>?`,
            () => {
                // Simular redirecionamento para tela de triagem
                showLoadingButton(event.target);
                setTimeout(() => {
                    window.location.href = `/colaborador/triagem/${id}`;
                }, 1000);
            }
        );
    }
    
    function inserirDoacao(id) {
        const donation = donations.find(d => d.id == id);
        if (!donation) return;
        
        showConfirmModal(
            'Registrar Doação',
            `Deseja registrar a doação para o doador <strong>${donation.doador.nome}</strong>?`,
            () => {
                // Simular processo de doação
                showLoadingButton(event.target);
                setTimeout(() => {
                    // Atualizar status
                    donation.status = 'aguardando_exames';
                    donation.dataDoacao = new Date().toISOString();
                    donation.volumeColetado = 450;
                    donation.medicoResponsavel = 'Dr. João Mendes';
                    
                    renderDonations();
                    
                    showSuccessAlert('Doação registrada com sucesso!');
                }, 2000);
            }
        );
    }
    
    function inserirExame(id) {
        const donation = donations.find(d => d.id == id);
        if (!donation) return;
        
        showConfirmModal(
            'Registrar Exames',
            `Deseja registrar os resultados dos exames para o doador <strong>${donation.doador.nome}</strong>?`,
            () => {
                // Simular processo de exames
                showLoadingButton(event.target);
                setTimeout(() => {
                    // Atualizar status
                    donation.status = 'concluida';
                    donation.dataConclusao = new Date().toISOString();
                    donation.examesAprovados = true;
                    donation.estoqueAtualizado = true;
                    
                    renderDonations();
                    
                    showSuccessAlert('Exames registrados e doação concluída!');
                }, 2000);
            }
        );
    }
    
    function gerarComprovante(id) {
        const donation = donations.find(d => d.id == id);
        if (!donation) return;
        
        showLoadingButton(event.target);
        setTimeout(() => {
            // Simular geração de comprovante
            const blob = new Blob(['Comprovante de doação simulado'], { type: 'text/plain' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `comprovante_doacao_${donation.doador.nome.replace(/\\s+/g, '_')}.txt`;
            a.click();
            window.URL.revokeObjectURL(url);
            
            showSuccessAlert('Comprovante gerado com sucesso!');
        }, 1000);
    }
    
    function verDetalhes(id) {
        const donation = donations.find(d => d.id == id);
        if (!donation) return;
        
        showDetailsModal(donation);
    }
    
    function verTriagem(id) {
        const donation = donations.find(d => d.id == id);
        if (!donation) return;
        
        showDetailsModal(donation, 'triagem');
    }
    
    function verDoacao(id) {
        const donation = donations.find(d => d.id == id);
        if (!donation) return;
        
        showDetailsModal(donation, 'doacao');
    }
    
    function verHistorico(id) {
        const donation = donations.find(d => d.id == id);
        if (!donation) return;
        
        showDetailsModal(donation, 'historico');
    }
    
    // Modal de detalhes
    function showDetailsModal(donation, view = 'geral') {
        const modalTitle = document.getElementById('detailsModalLabel');
        const modalContent = document.getElementById('modalDetailsContent');
        
        modalTitle.innerHTML = `<i class="fas fa-info-circle"></i> Detalhes da Doação - ${donation.doador.nome}`;
        
        let content = '';
        
        // Header com informações principais
        content += `
            <div class="modal-header-info">
                <div class="donor-avatar-large">
                    <i class="fas fa-user"></i>
                </div>
                <div class="donor-main-info">
                    <h4 class="donor-modal-name">${donation.doador.nome}</h4>
                    <div class="donor-key-details">
                        <span class="key-detail"><i class="fas fa-id-card"></i> ${donation.doador.cpf}</span>
                        <span class="key-detail"><i class="fas fa-tint"></i> ${donation.doador.tipoSanguineo}</span>
                        <span class="key-detail"><i class="fas fa-birthday-cake"></i> ${donation.doador.idade} anos</span>
                    </div>
                </div>
                <div class="status-info">
                    <div class="status-badge-modal ${getStatusConfig(donation.status).class}">
                        <i class="${getStatusConfig(donation.status).icon}"></i>
                        ${getStatusConfig(donation.status).text}
                    </div>
                    <small class="status-date">ID: #${donation.id}</small>
                </div>
            </div>
        `;
        
        // Seções organizadas em abas
        content += `
            <div class="modal-tabs">
                <button class="tab-btn active" data-tab="geral">
                    <i class="fas fa-user"></i> Dados Pessoais
                </button>
                <button class="tab-btn" data-tab="processo">
                    <i class="fas fa-route"></i> Processo
                </button>
                <button class="tab-btn" data-tab="observacoes">
                    <i class="fas fa-sticky-note"></i> Observações
                </button>
            </div>
        `;
        
        // Conteúdo das abas
        content += `<div class="modal-tab-content">`;
        
        // Aba Dados Pessoais
        content += `
            <div class="tab-panel active" id="tab-geral">
                <div class="info-cards-grid">
                    <div class="info-card">
                        <div class="info-card-header">
                            <i class="fas fa-address-card"></i>
                            <h6>Identificação</h6>
                        </div>
                        <div class="info-card-body">
                            <div class="info-row">
                                <span class="info-label">Nome Completo</span>
                                <span class="info-value">${donation.doador.nome}</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">CPF</span>
                                <span class="info-value">${donation.doador.cpf}</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">Idade</span>
                                <span class="info-value">${donation.doador.idade} anos</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="info-card">
                        <div class="info-card-header">
                            <i class="fas fa-phone"></i>
                            <h6>Contato</h6>
                        </div>
                        <div class="info-card-body">
                            <div class="info-row">
                                <span class="info-label">Telefone</span>
                                <span class="info-value">${donation.doador.telefone}</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">Cidade</span>
                                <span class="info-value">${donation.doador.cidade}</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="info-card">
                        <div class="info-card-header">
                            <i class="fas fa-heartbeat"></i>
                            <h6>Informações Médicas</h6>
                        </div>
                        <div class="info-card-body">
                            <div class="info-row">
                                <span class="info-label">Tipo Sanguíneo</span>
                                <span class="info-value blood-type">${donation.doador.tipoSanguineo}</span>
                            </div>
                            ${donation.doador.peso ? `
                                <div class="info-row">
                                    <span class="info-label">Peso</span>
                                    <span class="info-value">${donation.doador.peso} kg</span>
                                </div>
                            ` : ''}
                            ${donation.doador.altura ? `
                                <div class="info-row">
                                    <span class="info-label">Altura</span>
                                    <span class="info-value">${donation.doador.altura} cm</span>
                                </div>
                            ` : ''}
                            <div class="info-row">
                                <span class="info-label">Histórico</span>
                                <span class="info-value">${donation.doador.primeiraDoacao ? 'Primeira doação' : 'Doador regular'}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Aba Processo
        content += `
            <div class="tab-panel" id="tab-processo">
                <div class="process-timeline">
        `;
        
        // Timeline baseada no status
        const timelineItems = [];
        
        if (donation.dataAgendamento) {
            timelineItems.push({
                icon: 'fas fa-calendar',
                title: 'Agendamento',
                date: formatDateTime(donation.dataAgendamento),
                status: 'completed',
                description: 'Doação agendada no sistema'
            });
        }
        
        if (donation.dataTriagem) {
            timelineItems.push({
                icon: 'fas fa-clipboard-check',
                title: 'Triagem',
                date: formatDateTime(donation.dataTriagem),
                status: donation.triagemAprovada ? 'completed' : 'pending',
                description: donation.triagemAprovada ? 'Triagem aprovada' : 'Triagem pendente'
            });
        } else if (donation.status === 'aguardando_triagem') {
            timelineItems.push({
                icon: 'fas fa-clipboard-check',
                title: 'Triagem',
                date: 'Pendente',
                status: 'pending',
                description: 'Aguardando realização da triagem'
            });
        }
        
        if (donation.dataDoacao) {
            timelineItems.push({
                icon: 'fas fa-tint',
                title: 'Coleta',
                date: formatDateTime(donation.dataDoacao),
                status: 'completed',
                description: `${donation.volumeColetado}ml coletados - ${donation.medicoResponsavel}`
            });
        } else if (donation.status === 'aguardando_doacao') {
            timelineItems.push({
                icon: 'fas fa-tint',
                title: 'Coleta',
                date: 'Pendente',
                status: 'pending',
                description: 'Aguardando coleta de sangue'
            });
        }
        
        if (donation.dataConclusao) {
            timelineItems.push({
                icon: 'fas fa-check-circle',
                title: 'Concluída',
                date: formatDateTime(donation.dataConclusao),
                status: 'completed',
                description: 'Processo finalizado com sucesso'
            });
        } else if (donation.status === 'aguardando_exames') {
            timelineItems.push({
                icon: 'fas fa-vial',
                title: 'Exames',
                date: 'Em andamento',
                status: 'pending',
                description: 'Aguardando resultados dos exames'
            });
        }
        
        timelineItems.forEach((item, index) => {
            content += `
                <div class="timeline-item ${item.status}">
                    <div class="timeline-marker">
                        <i class="${item.icon}"></i>
                    </div>
                    <div class="timeline-content">
                        <h6 class="timeline-title">${item.title}</h6>
                        <p class="timeline-date">${item.date}</p>
                        <p class="timeline-description">${item.description}</p>
                    </div>
                </div>
            `;
        });
        
        content += `
                </div>
            </div>
        `;
        
        // Aba Observações
        content += `
            <div class="tab-panel" id="tab-observacoes">
                <div class="observations-section">
                    <div class="observation-card">
                        <div class="observation-header">
                            <i class="fas fa-sticky-note"></i>
                            <h6>Observações Gerais</h6>
                        </div>
                        <div class="observation-content">
                            ${donation.observacoes || 'Nenhuma observação registrada.'}
                        </div>
                    </div>
                    
                    <div class="quick-actions">
                        <h6><i class="fas fa-bolt"></i> Ações Rápidas</h6>
                        <div class="action-buttons-grid">
                            <button class="action-btn-modal primary" onclick="editDonation('${donation.id}')">
                                <i class="fas fa-edit"></i>
                                Editar Dados
                            </button>
                            <button class="action-btn-modal secondary" onclick="printDetails('${donation.id}')">
                                <i class="fas fa-print"></i>
                                Imprimir
                            </button>
                            <button class="action-btn-modal info" onclick="exportDetails('${donation.id}')">
                                <i class="fas fa-download"></i>
                                Exportar
                            </button>
                            <button class="action-btn-modal warning" onclick="addNote('${donation.id}')">
                                <i class="fas fa-plus"></i>
                                Add. Nota
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        content += `</div>`; // Fechar modal-tab-content
        
        modalContent.innerHTML = content;
        
        // Adicionar funcionalidade das abas
        setupModalTabs();
        
        detailsModal.show();
    }
    
    // Configurar funcionalidade das abas do modal
    function setupModalTabs() {
        const tabButtons = document.querySelectorAll('.tab-btn');
        const tabPanels = document.querySelectorAll('.tab-panel');
        
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetTab = button.getAttribute('data-tab');
                
                // Remover classe active de todos os botões e painéis
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabPanels.forEach(panel => panel.classList.remove('active'));
                
                // Adicionar classe active ao botão clicado e painel correspondente
                button.classList.add('active');
                const targetPanel = document.getElementById(`tab-${targetTab}`);
                if (targetPanel) {
                    targetPanel.classList.add('active');
                }
            });
        });
    }
    
    // Modal de confirmação
    function showConfirmModal(title, message, onConfirm) {
        const modalTitle = document.getElementById('confirmModalLabel');
        const modalBody = document.getElementById('confirmModalBody');
        const confirmBtn = document.getElementById('confirmActionBtn');
        
        modalTitle.textContent = title;
        modalBody.innerHTML = message;
        
        // Remover listeners anteriores
        const newConfirmBtn = confirmBtn.cloneNode(true);
        confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
        
        // Adicionar novo listener
        newConfirmBtn.addEventListener('click', () => {
            confirmModal.hide();
            onConfirm();
        });
        
        confirmModal.show();
    }
    
    // Alertas
    function showSuccessAlert(message) {
        const alert = document.createElement('div');
        alert.className = 'alert alert-success alert-dismissible fade show position-fixed';
        alert.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alert.innerHTML = `
            <i class="fas fa-check-circle me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alert);
        
        setTimeout(() => {
            if (alert.parentNode) {
                alert.parentNode.removeChild(alert);
            }
        }, 5000);
    }
    
    // Loading em botões
    function showLoadingButton(button) {
        if (!button) return;
        
        button.classList.add('loading');
        button.disabled = true;
        
        setTimeout(() => {
            button.classList.remove('loading');
            button.disabled = false;
        }, 3000);
    }
    
    // Utilitários
    function formatDateTime(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('pt-BR') + ' - ' + date.toLocaleTimeString('pt-BR', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }
    
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Expor funções globalmente para uso nos onclick
    window.fazerTriagem = fazerTriagem;
    window.inserirDoacao = inserirDoacao;
    window.inserirExame = inserirExame;
    window.gerarComprovante = gerarComprovante;
    window.verDetalhes = verDetalhes;
    window.verTriagem = verTriagem;
    window.verDoacao = verDoacao;
    window.verHistorico = verHistorico;
    
    // Funções adicionais para o modal
    window.editDonation = function(id) {
        showSuccessAlert('Funcionalidade de edição em desenvolvimento');
    };
    
    window.printDetails = function(id) {
        window.print();
    };
    
    window.exportDetails = function(id) {
        showSuccessAlert('Exportação em desenvolvimento');
    };
    
    window.addNote = function(id) {
        showSuccessAlert('Funcionalidade de notas em desenvolvimento');
    };
});

