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

document.addEventListener('DOMContentLoaded', function() {
    const fotoInput = document.getElementById('foto');
    const fotoAtual = document.getElementById('foto-atual');
    const previewContainer = document.getElementById('preview-foto-container');
    const previewFoto = document.getElementById('preview-foto');
    const btnAlterar = document.getElementById('btn-alterar');
    const btnCancelar = document.getElementById('btn-cancelar');

    fotoInput.addEventListener('change', function(e) {
        const file = e.target.files[0];

        if (file) {
            // Verificar se é uma imagem
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();

                reader.onload = function(e) {
                    // Esconder foto atual e mostrar preview
                    fotoAtual.style.display = 'none';
                    previewFoto.src = e.target.result;
                    previewContainer.style.display = 'block';

                    // Habilitar botão e mostrar opções
                    btnAlterar.disabled = false;
                    btnAlterar.innerHTML = '<i class="bi-check"></i> Confirmar Alteração';
                    btnCancelar.style.display = 'inline-block';
                };

                reader.readAsDataURL(file);  // ← Converte arquivo em URL para preview
            } else {
                alert('Por favor, selecione apenas arquivos de imagem.');
                cancelarSelecao();
            }
        } else {
            cancelarSelecao();
        }
    });
});

function cancelarSelecao() {
    const fotoInput = document.getElementById('foto');
    const fotoAtual = document.getElementById('foto-atual');
    const previewContainer = document.getElementById('preview-foto-container');
    const btnAlterar = document.getElementById('btn-alterar');
    const btnCancelar = document.getElementById('btn-cancelar');

    // Limpar seleção e voltar ao estado inicial
    fotoInput.value = '';
    fotoAtual.style.display = 'block';
    previewContainer.style.display = 'none';
    btnAlterar.disabled = true;
    btnAlterar.innerHTML = '<i class="bi-camera"></i> Alterar Foto';
    btnCancelar.style.display = 'none';
}