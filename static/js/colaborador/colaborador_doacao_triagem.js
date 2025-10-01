// Triagem de Doação - JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const form = document.getElementById('triagemForm');
    const sections = document.querySelectorAll('.form-section');
    const progressBar = document.getElementById('progressBar');
    const progressPercentage = document.getElementById('progressPercentage');
    const progressSteps = document.querySelectorAll('.step');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');
    const resultModal = new bootstrap.Modal(document.getElementById('resultModal'));
    
    // Variáveis de estado
    let currentSection = 1;
    const totalSections = sections.length;
    let formData = {};
    let triagemResult = null;
    
    // Critérios de impedimento
    const impedimentos = {
        temporarios: [
            { campo: 'jejum', valor: 'sim', motivo: 'Não é necessário estar em jejum para doação de sangue' },
            { campo: 'alcool_12h', valor: 'sim', motivo: 'Consumo de álcool nas últimas 12 horas' },
            { campo: 'atividade_fisica_12h', valor: 'sim', motivo: 'Atividade física intensa nas últimas 12 horas' },
            { campo: 'sono_6h', valor: 'nao', motivo: 'Sono insuficiente (menos de 6 horas)' },
            { campo: 'sintomas_gripais', valor: 'sim', motivo: 'Presença de sintomas gripais' },
            { campo: 'procedimentos_6m', valor: 'sim', motivo: 'Procedimentos invasivos nos últimos 6 meses' }
        ],
        permanentes: [
            { campo: 'diabetes', valor: 'sim', motivo: 'Diabetes' },
            { campo: 'cancer', valor: 'sim', motivo: 'Histórico de câncer' },
            { campo: 'hepatite', valor: 'sim', motivo: 'Hepatite' },
            { campo: 'drogas_ilicitas', valor: 'sim', motivo: 'Uso de drogas ilícitas' },
            { campo: 'risco_ist', valor: 'sim', motivo: 'Situações de risco para IST' }
        ],
        avaliacaoMedica: [
            { campo: 'hipertensao', valor: 'sim', motivo: 'Hipertensão arterial' },
            { campo: 'cardiopatia', valor: 'sim', motivo: 'Cardiopatia' },
            { campo: 'outras_condicoes', valor: 'sim', motivo: 'Outras condições médicas' },
            { campo: 'medicamentos', valor: 'sim', motivo: 'Uso de medicamentos' }
        ]
    };
    
    // Inicialização
    init();
    
    function init() {
        setupEventListeners();
        updateProgress();
        setupConditionalFields();
        setupValidation();
        loadDraft();
    }
    
    // Configurar Event Listeners
    function setupEventListeners() {
        // Navegação
        nextBtn.addEventListener('click', nextSection);
        prevBtn.addEventListener('click', prevSection);
        form.addEventListener('submit', handleSubmit);
        
        // Validação em tempo real
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                validateField(this);
                updateQuestionCard(this);
                saveAsDraft();
            });
        });
        
        // Máscara para telefone
        const telefoneInput = document.getElementById('telefone_emergencia');
        if (telefoneInput) {
            telefoneInput.addEventListener('input', formatPhone);
        }
        
        // Validação de peso e altura
        const pesoInput = document.getElementById('peso');
        const alturaInput = document.getElementById('altura');
        
        if (pesoInput) {
            pesoInput.addEventListener('input', validatePhysicalData);
        }
        
        if (alturaInput) {
            alturaInput.addEventListener('input', validatePhysicalData);
        }
    }
    
    // Configurar campos condicionais
    function setupConditionalFields() {
        // Outras condições médicas
        const outrasCondicoes = document.querySelectorAll('input[name="outras_condicoes"]');
        const outrasCondicoesDetalhes = document.getElementById('outras_condicoes_detalhes');
        
        outrasCondicoes.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.value === 'sim') {
                    outrasCondicoesDetalhes.style.display = 'block';
                    outrasCondicoesDetalhes.querySelector('textarea').required = true;
                } else {
                    outrasCondicoesDetalhes.style.display = 'none';
                    outrasCondicoesDetalhes.querySelector('textarea').required = false;
                    outrasCondicoesDetalhes.querySelector('textarea').value = '';
                }
            });
        });
        
        // Medicamentos
        const medicamentos = document.querySelectorAll('input[name="medicamentos"]');
        const medicamentosDetalhes = document.getElementById('medicamentos_detalhes');
        
        medicamentos.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.value === 'sim') {
                    medicamentosDetalhes.style.display = 'block';
                    medicamentosDetalhes.querySelector('textarea').required = true;
                } else {
                    medicamentosDetalhes.style.display = 'none';
                    medicamentosDetalhes.querySelector('textarea').required = false;
                    medicamentosDetalhes.querySelector('textarea').value = '';
                }
            });
        });
        
        // Procedimentos
        const procedimentos = document.querySelectorAll('input[name="procedimentos_6m"]');
        const procedimentosDetalhes = document.getElementById('procedimentos_detalhes');
        
        procedimentos.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.value === 'sim') {
                    procedimentosDetalhes.style.display = 'block';
                    procedimentosDetalhes.querySelector('textarea').required = true;
                } else {
                    procedimentosDetalhes.style.display = 'none';
                    procedimentosDetalhes.querySelector('textarea').required = false;
                    procedimentosDetalhes.querySelector('textarea').value = '';
                }
            });
        });
    }
    
    // Configurar validação
    function setupValidation() {
        // Validação customizada para campos numéricos
        const numericInputs = document.querySelectorAll('input[type="number"]');
        numericInputs.forEach(input => {
            input.addEventListener('input', function() {
                const value = parseFloat(this.value);
                const min = parseFloat(this.min);
                const max = parseFloat(this.max);
                
                if (value < min || value > max) {
                    this.classList.add('is-invalid');
                } else {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                }
            });
        });
    }
    
    // Formatação de telefone
    function formatPhone(event) {
        let value = event.target.value.replace(/\D/g, '');
        
        if (value.length <= 11) {
            value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
            if (value.length < 14) {
                value = value.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
            }
        }
        
        event.target.value = value;
    }
    
    // Validar dados físicos
    function validatePhysicalData() {
        const peso = parseFloat(document.getElementById('peso').value);
        const altura = parseFloat(document.getElementById('altura').value);
        
        if (peso && altura) {
            const imc = peso / ((altura / 100) ** 2);
            
            // Verificar critérios mínimos
            if (peso < 50) {
                showFieldWarning('peso', 'Peso mínimo para doação: 50kg');
            } else if (altura < 140) {
                showFieldWarning('altura', 'Altura mínima para doação: 140cm');
            } else if (imc < 16 || imc > 40) {
                showFieldWarning('peso', `IMC fora da faixa recomendada: ${imc.toFixed(1)}`);
            } else {
                clearFieldWarnings(['peso', 'altura']);
            }
        }
    }
    
    // Mostrar aviso de campo
    function showFieldWarning(fieldId, message) {
        const field = document.getElementById(fieldId);
        const existingWarning = field.parentNode.querySelector('.field-warning');
        
        if (existingWarning) {
            existingWarning.textContent = message;
        } else {
            const warning = document.createElement('div');
            warning.className = 'field-warning text-warning mt-1';
            warning.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${message}`;
            field.parentNode.appendChild(warning);
        }
    }
    
    // Limpar avisos de campo
    function clearFieldWarnings(fieldIds) {
        fieldIds.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            const warning = field.parentNode.querySelector('.field-warning');
            if (warning) {
                warning.remove();
            }
        });
    }
    
    // Validar campo individual
    function validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        
        // Validações específicas por tipo
        if (field.required && !value) {
            isValid = false;
        }
        
        if (field.type === 'email' && value && !isValidEmail(value)) {
            isValid = false;
        }
        
        if (field.type === 'tel' && value && !isValidPhone(value)) {
            isValid = false;
        }
        
        // Aplicar classes de validação
        if (isValid) {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
        } else {
            field.classList.remove('is-valid');
            field.classList.add('is-invalid');
        }
        
        return isValid;
    }
    
    // Atualizar card da pergunta
    function updateQuestionCard(input) {
        const questionCard = input.closest('.question-card');
        if (questionCard && input.type === 'radio' && input.checked) {
            questionCard.classList.add('answered');
        }
    }
    
    // Validações auxiliares
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    function isValidPhone(phone) {
        const phoneRegex = /^\(\d{2}\)\s\d{4,5}-\d{4}$/;
        return phoneRegex.test(phone);
    }
    
    // Navegação entre seções
    function nextSection() {
        if (validateCurrentSection()) {
            if (currentSection < totalSections) {
                currentSection++;
                showSection(currentSection);
                
                if (currentSection === totalSections) {
                    generateSummary();
                }
            }
        } else {
            showAlert('Atenção', 'Por favor, preencha todos os campos obrigatórios antes de continuar.', 'warning');
        }
    }
    
    function prevSection() {
        if (currentSection > 1) {
            currentSection--;
            showSection(currentSection);
        }
    }
    
    function showSection(sectionNumber) {
        // Ocultar todas as seções
        sections.forEach(section => {
            section.classList.remove('active');
        });
        
        // Mostrar seção atual
        const targetSection = document.getElementById(`section${sectionNumber}`);
        if (targetSection) {
            targetSection.classList.add('active');
        }
        
        // Atualizar botões
        updateNavigationButtons();
        
        // Atualizar progresso
        updateProgress();
        
        // Scroll para o topo
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    function updateNavigationButtons() {
        // Botão anterior
        if (currentSection === 1) {
            prevBtn.style.display = 'none';
        } else {
            prevBtn.style.display = 'inline-flex';
        }
        
        // Botão próximo/finalizar
        if (currentSection === totalSections) {
            nextBtn.style.display = 'none';
            submitBtn.style.display = 'inline-flex';
        } else {
            nextBtn.style.display = 'inline-flex';
            submitBtn.style.display = 'none';
        }
    }
    
    // Atualizar progresso
    function updateProgress() {
        const progress = ((currentSection - 1) / (totalSections - 1)) * 100;
        progressBar.style.width = `${progress}%`;
        progressPercentage.textContent = `${Math.round(progress)}%`;
        
        // Atualizar steps
        progressSteps.forEach((step, index) => {
            const stepNumber = index + 1;
            
            if (stepNumber < currentSection) {
                step.classList.add('completed');
                step.classList.remove('active');
            } else if (stepNumber === currentSection) {
                step.classList.add('active');
                step.classList.remove('completed');
            } else {
                step.classList.remove('active', 'completed');
            }
        });
    }
    
    // Validar seção atual
    function validateCurrentSection() {
        const currentSectionElement = document.getElementById(`section${currentSection}`);
        const requiredFields = currentSectionElement.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (field.type === 'radio') {
                const radioGroup = currentSectionElement.querySelectorAll(`input[name="${field.name}"]`);
                const isChecked = Array.from(radioGroup).some(radio => radio.checked);
                if (!isChecked) {
                    isValid = false;
                    // Destacar grupo de radio não preenchido
                    const questionCard = field.closest('.question-card');
                    if (questionCard) {
                        questionCard.style.borderColor = 'var(--hemotec-danger)';
                        setTimeout(() => {
                            questionCard.style.borderColor = '';
                        }, 3000);
                    }
                }
            } else if (!field.value.trim()) {
                isValid = false;
                validateField(field);
            }
        });
        
        return isValid;
    }
    
    // Gerar resumo
    function generateSummary() {
        const summaryContainer = document.getElementById('summaryContainer');
        formData = collectFormData();
        
        const summaryHTML = `
            <div class="summary-section">
                <h5 class="summary-title">
                    <i class="fas fa-user"></i>
                    Dados Pessoais
                </h5>
                <div class="summary-item">
                    <span class="summary-question">Altura:</span>
                    <span class="summary-answer neutral">${formData.altura} cm</span>
                </div>
                <div class="summary-item">
                    <span class="summary-question">Peso:</span>
                    <span class="summary-answer neutral">${formData.peso} kg</span>
                </div>
                <div class="summary-item">
                    <span class="summary-question">Profissão:</span>
                    <span class="summary-answer neutral">${formData.profissao}</span>
                </div>
            </div>
            
            <div class="summary-section">
                <h5 class="summary-title">
                    <i class="fas fa-heartbeat"></i>
                    Condições de Saúde
                </h5>
                <div class="summary-item">
                    <span class="summary-question">Em jejum:</span>
                    <span class="summary-answer ${formData.jejum === 'sim' ? 'sim' : 'nao'}">${formData.jejum === 'sim' ? 'Sim' : 'Não'}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-question">Diabetes:</span>
                    <span class="summary-answer ${formData.diabetes}">${formData.diabetes === 'sim' ? 'Sim' : 'Não'}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-question">Hipertensão:</span>
                    <span class="summary-answer ${formData.hipertensao}">${formData.hipertensao === 'sim' ? 'Sim' : 'Não'}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-question">Cardiopatia:</span>
                    <span class="summary-answer ${formData.cardiopatia}">${formData.cardiopatia === 'sim' ? 'Sim' : 'Não'}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-question">Câncer:</span>
                    <span class="summary-answer ${formData.cancer}">${formData.cancer === 'sim' ? 'Sim' : 'Não'}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-question">Hepatite:</span>
                    <span class="summary-answer ${formData.hepatite}">${formData.hepatite === 'sim' ? 'Sim' : 'Não'}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-question">Sintomas gripais:</span>
                    <span class="summary-answer ${formData.sintomas_gripais}">${formData.sintomas_gripais === 'sim' ? 'Sim' : 'Não'}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-question">Outras condições médicas:</span>
                    <span class="summary-answer ${formData.outras_condicoes}">${formData.outras_condicoes === 'sim' ? 'Sim' : 'Não'}</span>
                </div>
                ${formData.outras_condicoes === 'sim' && formData.outras_condicoes_texto ? `
                <div class="summary-item text-item">
                    <span class="summary-question">Detalhes das condições:</span>
                    <span class="summary-answer neutral">${formData.outras_condicoes_texto}</span>
                </div>
                ` : ''}
                <div class="summary-item">
                    <span class="summary-question">Uso de medicamentos:</span>
                    <span class="summary-answer ${formData.medicamentos}">${formData.medicamentos === 'sim' ? 'Sim' : 'Não'}</span>
                </div>
                ${formData.medicamentos === 'sim' && formData.medicamentos_texto ? `
                <div class="summary-item text-item">
                    <span class="summary-question">Medicamentos em uso:</span>
                    <span class="summary-answer neutral">${formData.medicamentos_texto}</span>
                </div>
                ` : ''}
            </div>
            
            <div class="summary-section">
                <h5 class="summary-title">
                    <i class="fas fa-running"></i>
                    Estilo de Vida
                </h5>
                <div class="summary-item">
                    <span class="summary-question">Fumante:</span>
                    <span class="summary-answer ${formData.fumante === 'sim' ? 'sim' : 'nao'}">${getFumanteText(formData.fumante)}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-question">Álcool (12h):</span>
                    <span class="summary-answer ${formData.alcool_12h}">${formData.alcool_12h === 'sim' ? 'Sim' : 'Não'}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-question">Drogas ilícitas:</span>
                    <span class="summary-answer ${formData.drogas_ilicitas}">${formData.drogas_ilicitas === 'sim' ? 'Sim' : 'Não'}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-question">Atividade física (12h):</span>
                    <span class="summary-answer ${formData.atividade_fisica_12h}">${formData.atividade_fisica_12h === 'sim' ? 'Sim' : 'Não'}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-question">Sono adequado:</span>
                    <span class="summary-answer ${formData.sono_6h === 'sim' ? 'nao' : 'sim'}">${formData.sono_6h === 'sim' ? 'Sim' : 'Não'}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-question">Procedimentos (6 meses):</span>
                    <span class="summary-answer ${formData.procedimentos_6m}">${formData.procedimentos_6m === 'sim' ? 'Sim' : 'Não'}</span>
                </div>
                ${formData.procedimentos_6m === 'sim' && formData.procedimentos_texto ? `
                <div class="summary-item text-item">
                    <span class="summary-question">Procedimentos realizados:</span>
                    <span class="summary-answer neutral">${formData.procedimentos_texto}</span>
                </div>
                ` : ''}
            </div>
        `;
        
        summaryContainer.innerHTML = summaryHTML;
    }
    
    function getFumanteText(value) {
        switch (value) {
            case 'sim': return 'Sim';
            case 'nao': return 'Não';
            case 'ex-fumante': return 'Ex-fumante';
            default: return value;
        }
    }
    
    // Coletar dados do formulário
    function collectFormData() {
        const data = {};
        const formElements = form.querySelectorAll('input, textarea, select');
        
        formElements.forEach(element => {
            if (element.type === 'radio') {
                if (element.checked) {
                    data[element.name] = element.value;
                }
            } else if (element.type === 'checkbox') {
                data[element.name] = element.checked;
            } else {
                data[element.name] = element.value;
            }
        });
        
        return data;
    }
    
    // Analisar aptidão para doação
    function analyzeAptitude(data) {
        const result = {
            status: 'apto', // apto, inapto_temporario, inapto_permanente, avaliacao_medica
            impedimentos: [],
            recomendacoes: []
        };
        
        // Verificar impedimentos permanentes
        impedimentos.permanentes.forEach(impedimento => {
            if (data[impedimento.campo] === impedimento.valor) {
                result.status = 'inapto_permanente';
                result.impedimentos.push(impedimento.motivo);
            }
        });
        
        // Se não há impedimentos permanentes, verificar temporários
        if (result.status === 'apto') {
            impedimentos.temporarios.forEach(impedimento => {
                if (data[impedimento.campo] === impedimento.valor) {
                    result.status = 'inapto_temporario';
                    result.impedimentos.push(impedimento.motivo);
                }
            });
        }
        
        // Se ainda apto, verificar se precisa de avaliação médica
        if (result.status === 'apto') {
            impedimentos.avaliacaoMedica.forEach(impedimento => {
                if (data[impedimento.campo] === impedimento.valor) {
                    result.status = 'avaliacao_medica';
                    result.impedimentos.push(impedimento.motivo);
                }
            });
        }
        
        // Verificar dados físicos
        const peso = parseFloat(data.peso);
        const altura = parseFloat(data.altura);
        
        if (peso < 50) {
            result.status = 'inapto_temporario';
            result.impedimentos.push('Peso abaixo do mínimo (50kg)');
        }
        
        if (altura < 140) {
            result.status = 'inapto_temporario';
            result.impedimentos.push('Altura abaixo do mínimo (140cm)');
        }
        
        // Gerar recomendações
        generateRecommendations(result, data);
        
        return result;
    }
    
    // Gerar recomendações
    function generateRecommendations(result, data) {
        switch (result.status) {
            case 'apto':
                result.recomendacoes = [
                    'Mantenha-se hidratado antes da doação',
                    'Faça uma refeição leve e nutritiva antes de vir ao hemocentro',
                    'NÃO é necessário estar em jejum para doar sangue',
                    'Traga um documento com foto',
                    'Evite atividades físicas intensas após a doação'
                ];
                break;
                
            case 'inapto_temporario':
                result.recomendacoes = [
                    'Aguarde o período necessário antes de tentar doar novamente',
                    'Mantenha hábitos saudáveis',
                    'Consulte um médico se necessário'
                ];
                
                // Recomendações específicas
                if (data.jejum === 'sim') {
                    result.recomendacoes.push('Não é necessário estar em jejum. Faça uma refeição leve antes da doação');
                }
                if (data.alcool_12h === 'sim') {
                    result.recomendacoes.push('Aguarde 12 horas sem consumir álcool');
                }
                if (data.sono_6h === 'nao') {
                    result.recomendacoes.push('Tenha uma boa noite de sono (mínimo 6 horas)');
                }
                break;
                
            case 'inapto_permanente':
                result.recomendacoes = [
                    'Infelizmente você não pode doar sangue devido às condições identificadas',
                    'Consulte um médico para mais informações',
                    'Considere outras formas de ajudar, como divulgar campanhas de doação'
                ];
                break;
                
            case 'avaliacao_medica':
                result.recomendacoes = [
                    'Será necessária uma avaliação médica no hemocentro',
                    'Traga seus exames médicos recentes',
                    'Liste todos os medicamentos que você usa',
                    'O médico decidirá sobre sua aptidão para doação'
                ];
                break;
        }
    }
    
    // Submeter formulário
    function handleSubmit(event) {
        event.preventDefault();
        
        if (!validateCurrentSection()) {
            showAlert('Erro', 'Por favor, preencha todos os campos obrigatórios.', 'error');
            return;
        }
        
        // Verificar termos
        const termos = document.getElementById('termos');
        if (!termos.checked) {
            showAlert('Atenção', 'Você deve aceitar os termos para continuar.', 'warning');
            return;
        }
        
        // Mostrar loading
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;
        
        // Simular processamento
        setTimeout(() => {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
            
            // Analisar aptidão
            formData = collectFormData();
            triagemResult = analyzeAptitude(formData);
            
            // Mostrar resultado
            showResult(triagemResult);
            
            // Limpar rascunho
            localStorage.removeItem('triagem_rascunho');
        }, 2000);
    }
    
    // Mostrar resultado
    function showResult(result) {
        const resultHeader = document.getElementById('resultHeader');
        const resultBody = document.getElementById('resultBody');
        const continueBtn = document.getElementById('continueBtn');
        
        let headerClass, iconClass, title, description;
        
        switch (result.status) {
            case 'apto':
                headerClass = 'success';
                iconClass = 'success';
                title = 'Parabéns! Você está apto para doação!';
                description = 'Sua triagem foi aprovada. Você pode prosseguir com o agendamento da doação.';
                continueBtn.style.display = 'inline-block';
                break;
                
            case 'inapto_temporario':
                headerClass = 'warning';
                iconClass = 'warning';
                title = 'Impedimento Temporário';
                description = 'Você possui alguns impedimentos temporários para doação. Siga as recomendações e tente novamente mais tarde.';
                continueBtn.style.display = 'none';
                break;
                
            case 'inapto_permanente':
                headerClass = 'danger';
                iconClass = 'danger';
                title = 'Impedimento Permanente';
                description = 'Infelizmente você não pode doar sangue devido às condições identificadas.';
                continueBtn.style.display = 'none';
                break;
                
            case 'avaliacao_medica':
                headerClass = 'warning';
                iconClass = 'warning';
                title = 'Avaliação Médica Necessária';
                description = 'Será necessária uma avaliação médica no hemocentro para determinar sua aptidão.';
                continueBtn.style.display = 'inline-block';
                break;
        }
        
        // Atualizar header
        resultHeader.className = `modal-header ${headerClass}`;
        
        // Gerar conteúdo do body
        const impedimentosList = result.impedimentos.length > 0 
            ? `<ul>${result.impedimentos.map(imp => `<li>${imp}</li>`).join('')}</ul>`
            : '';
            
        const recomendacoesList = result.recomendacoes.length > 0
            ? `<ul>${result.recomendacoes.map(rec => `<li>${rec}</li>`).join('')}</ul>`
            : '';
        
        resultBody.innerHTML = `
            <div class="result-content">
                <div class="result-icon ${iconClass}">
                    <i class="fas fa-${result.status === 'apto' ? 'check-circle' : result.status === 'inapto_permanente' ? 'times-circle' : 'exclamation-triangle'}"></i>
                </div>
                <h4 class="result-title">${title}</h4>
                <p class="result-description">${description}</p>
                
                ${result.impedimentos.length > 0 ? `
                    <div class="result-recommendations">
                        <h6><i class="fas fa-exclamation-triangle text-warning"></i> Impedimentos Identificados:</h6>
                        ${impedimentosList}
                    </div>
                ` : ''}
                
                ${result.recomendacoes.length > 0 ? `
                    <div class="result-recommendations">
                        <h6><i class="fas fa-lightbulb text-info"></i> Recomendações:</h6>
                        ${recomendacoesList}
                    </div>
                ` : ''}
            </div>
        `;
        
        // Configurar botão continuar
        if (continueBtn.style.display !== 'none') {
            continueBtn.onclick = function() {
                resultModal.hide();
                // Redirecionar para agendamento
                setTimeout(() => {
                    window.location.href = '/doador/agendamento/adicionar';
                }, 500);
            };
        }
        
        // Mostrar modal
        resultModal.show();
    }
    
    // Salvar rascunho
    function saveAsDraft() {
        const draftData = {
            currentSection: currentSection,
            formData: collectFormData(),
            timestamp: new Date().toISOString()
        };
        
        localStorage.setItem('triagem_rascunho', JSON.stringify(draftData));
    }
    
    // Carregar rascunho
    function loadDraft() {
        const draft = localStorage.getItem('triagem_rascunho');
        if (draft) {
            const draftData = JSON.parse(draft);
            
            // Verificar se o rascunho não é muito antigo (24 horas)
            const draftAge = new Date() - new Date(draftData.timestamp);
            if (draftAge < 24 * 60 * 60 * 1000) {
                if (confirm('Encontramos um rascunho salvo da triagem. Deseja carregá-lo?')) {
                    // Restaurar dados do formulário
                    Object.keys(draftData.formData).forEach(key => {
                        const element = form.querySelector(`[name="${key}"]`);
                        if (element) {
                            if (element.type === 'radio') {
                                const radio = form.querySelector(`[name="${key}"][value="${draftData.formData[key]}"]`);
                                if (radio) {
                                    radio.checked = true;
                                    updateQuestionCard(radio);
                                }
                            } else if (element.type === 'checkbox') {
                                element.checked = draftData.formData[key];
                            } else {
                                element.value = draftData.formData[key];
                            }
                        }
                    });
                    
                    // Restaurar seção atual
                    currentSection = draftData.currentSection || 1;
                    showSection(currentSection);
                    
                    // Reconfigurar campos condicionais
                    setupConditionalFields();
                }
            }
        }
    }
    
    // Mostrar alerta
    function showAlert(title, message, type = 'info') {
        const alertModal = document.createElement('div');
        alertModal.className = 'modal fade';
        alertModal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header bg-${type === 'error' ? 'danger' : type === 'warning' ? 'warning' : 'info'} text-white">
                        <h5 class="modal-title">
                            <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : type === 'warning' ? 'exclamation-circle' : 'info-circle'}"></i>
                            ${title}
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>${message}</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(alertModal);
        const modal = new bootstrap.Modal(alertModal);
        modal.show();
        
        alertModal.addEventListener('hidden.bs.modal', () => {
            document.body.removeChild(alertModal);
        });
    }
    
    // Utilitários
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
    
    // Salvar rascunho com debounce
    const debouncedSave = debounce(saveAsDraft, 1000);
    
    // Adicionar listener para salvar rascunho automaticamente
    form.addEventListener('input', debouncedSave);
    form.addEventListener('change', debouncedSave);
});

