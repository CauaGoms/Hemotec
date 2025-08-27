function editProfile() {
    alert('Abrindo edição de perfil...');
    // Implementar lógica para edição do perfil
}

function editHealthInfo() {
    alert('Abrindo edição de informações de saúde...');
    // Implementar lógica para edição das informações de saúde
}

function editProfessionalInfo() {
    alert('Abrindo edição de informações profissionais...');
    // Implementar lógica para edição das informações profissionais
}

function changePassword() {
    alert('Abrindo formulário para alteração de senha...');
    // Implementar lógica para alteração de senha
}

function confirmAccountDeletion() {
    if (confirm('Tem certeza que deseja encerrar sua conta? Esta ação é irreversível e todos os seus dados serão permanentemente removidos.')) {
        alert('Sua conta será encerrada. Você será redirecionado para a página inicial.');
        // Implementar lógica para encerramento de conta
        // window.location.href = 'login.html';
    }
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

// Ativar tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});