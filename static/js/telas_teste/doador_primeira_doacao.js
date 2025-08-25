let currentStep = 1;
const totalSteps = 4;

// Inicializar data mínima para agendamento
document.addEventListener('DOMContentLoaded', function () {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    const dateInput = document.getElementById('dataDoacao');
    dateInput.min = tomorrow.toISOString().split('T')[0];

    // Máximo 30 dias no futuro
    const maxDate = new Date(today);
    maxDate.setDate(maxDate.getDate() + 30);
    dateInput.max = maxDate.toISOString().split('T')[0];

    // Verificar elegibilidade inicial
    checkEligibility();
});

function changeStep(direction) {
    if (direction === 1 && !validateCurrentStep()) {
        return;
    }

    // Esconder seção atual
    document.getElementById(`section${currentStep}`).style.display = 'none';

    // Atualizar step
    currentStep += direction;

    // Mostrar nova seção
    document.getElementById(`section${currentStep}`).style.display = 'block';

    // Atualizar indicador de progresso
    updateProgressIndicator();

    // Atualizar botões
    updateButtons();

    // Se chegou na última seção, gerar resumo
    if (currentStep === 4) {
        generateSummary();
    }

    // Scroll para o topo
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function updateProgressIndicator() {
    for (let i = 1; i <= totalSteps; i++) {
        const step = document.querySelector(`.step:nth-child(${i})`);
        if (i < currentStep) {
            step.classList.add('completed');
            step.classList.remove('active');
        } else if (i === currentStep) {
            step.classList.add('active');
            step.classList.remove('completed');
        } else {
            step.classList.remove('active', 'completed');
        }
    }
}

function updateButtons() {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');

    prevBtn.style.display = currentStep > 1 ? 'block' : 'none';
    nextBtn.style.display = currentStep < totalSteps ? 'block' : 'none';
    submitBtn.style.display = currentStep === totalSteps ? 'block' : 'none';
}

function validateCurrentStep() {
    const currentSection = document.getElementById(`section${currentStep}`);
    const requiredFields = currentSection.querySelectorAll('[required]');

    for (let field of requiredFields) {
        if (!field.value.trim()) {
            field.focus();
            field.classList.add('is-invalid');
            return false;
        } else {
            field.classList.remove('is-invalid');
        }
    }

    return true;
}

function checkEligibility() {
    // Verificar idade (assumindo que já foi validada no cadastro inicial)
    const ageCard = document.getElementById('eligibility-age');
    ageCard.classList.add('valid');
    ageCard.querySelector('.fa-check-circle').style.display = 'block';

    // Verificar peso
    const pesoInput = document.getElementById('peso');
    pesoInput.addEventListener('input', function () {
        const weightCard = document.getElementById('eligibility-weight');
        const peso = parseFloat(this.value);

        if (peso >= 50) {
            weightCard.classList.remove('invalid');
            weightCard.classList.add('valid');
            weightCard.querySelector('.fa-check-circle').style.display = 'block';
            weightCard.querySelector('.fa-times-circle').style.display = 'none';
        } else {
            weightCard.classList.remove('valid');
            weightCard.classList.add('invalid');
            weightCard.querySelector('.fa-check-circle').style.display = 'none';
            weightCard.querySelector('.fa-times-circle').style.display = 'block';
        }
    });
}

function generateSummary() {
    const summary = document.getElementById('summary');
    const altura = document.getElementById('altura').value;
    const peso = document.getElementById('peso').value;
    const tipoSanguineo = document.getElementById('tipoSanguineo').value || 'A determinar';
    const profissao = document.getElementById('profissao').value;

    summary.innerHTML = `
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>Altura:</strong> ${altura} cm</p>
                        <p><strong>Peso:</strong> ${peso} kg</p>
                        <p><strong>Tipo Sanguíneo:</strong> ${tipoSanguineo}</p>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Profissão:</strong> ${profissao}</p>
                        <p><strong>Status:</strong> <span class="badge bg-success">Apto para doação</span></p>
                    </div>
                </div>
            `;
}

// Máscara para telefone
document.getElementById('telefoneEmergencia').addEventListener('input', function (e) {
    let value = e.target.value.replace(/\D/g, '');
    value = value.replace(/(\d{2})(\d)/, '($1) $2');
    value = value.replace(/(\d{5})(\d)/, '$1-$2');
    e.target.value = value;
});

// Checkbox "nenhuma" exclusivo
document.getElementById('nenhuma').addEventListener('change', function () {
    if (this.checked) {
        const otherCheckboxes = ['diabetes', 'hipertensao', 'cardiopatia', 'epilepsia', 'cancer'];
        otherCheckboxes.forEach(id => {
            document.getElementById(id).checked = false;
        });
    }
});

// Desmarcar "nenhuma" se outro for marcado
['diabetes', 'hipertensao', 'cardiopatia', 'epilepsia', 'cancer'].forEach(id => {
    document.getElementById(id).addEventListener('change', function () {
        if (this.checked) {
            document.getElementById('nenhuma').checked = false;
        }
    });
});

// Submit do formulário
document.getElementById('donationForm').addEventListener('submit', function (e) {
    e.preventDefault();

    if (!validateCurrentStep()) {
        return;
    }

    // Simular envio
    const submitBtn = document.getElementById('submitBtn');
    const originalText = submitBtn.innerHTML;

    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processando...';
    submitBtn.disabled = true;

    setTimeout(() => {
        alert('Cadastro realizado com sucesso! Você receberá uma confirmação por email.');
        window.location.href = 'dashboard.html';
    }, 2000);
});

// Animações de entrada
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
        }
    });
});

document.querySelectorAll('.form-section').forEach(section => {
    observer.observe(section);
});