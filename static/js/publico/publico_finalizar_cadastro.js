let cadastroStep = 1;
const cadastroTotalSteps = 3;

function cadastroChangeStep(direction) {
    if (direction === 1 && !cadastroValidateCurrentStep()) {
        return;
    }
    document.getElementById(`cadastroSection${cadastroStep}`).style.display = 'none';
    cadastroStep += direction;
    document.getElementById(`cadastroSection${cadastroStep}`).style.display = 'block';
    cadastroUpdateButtons();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function cadastroUpdateButtons() {
    document.getElementById('cadastroPrevBtn').style.display = cadastroStep > 1 ? 'block' : 'none';
    document.getElementById('cadastroNextBtn').style.display = cadastroStep < cadastroTotalSteps ? 'block' : 'none';
    document.getElementById('cadastroSubmitBtn').style.display = cadastroStep === cadastroTotalSteps ? 'block' : 'none';

    const nextBtn = document.getElementById('cadastroNextBtn');
    if (cadastroStep === 2) {
        nextBtn.classList.add('btn-small');
    } else {
        nextBtn.classList.remove('btn-small');
    }
}

function cadastroValidateCurrentStep() {
    const currentSection = document.getElementById(`cadastroSection${cadastroStep}`);
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

    if (cadastroStep === 3) {
        const senha = document.getElementById('senha').value;
        const confirmar = document.getElementById('confirmar_senha').value;
        if (senha !== confirmar) {
            alert('As senhas não coincidem!');
            return false;
        }
        if (senha.length < 6) {
            alert('A senha deve ter pelo menos 6 caracteres.');
            return false;
        }
    }
    return true;
}

// Máscara simples para CPF do gestor
document.getElementById('cpf_gestor').addEventListener('input', function (e) {
    let value = e.target.value.replace(/\D/g, '');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    e.target.value = value;
});

// Máscara simples para CNPJ
document.getElementById('cnpj_instituicao').addEventListener('input', function (e) {
    let value = e.target.value.replace(/\D/g, '');
    value = value.replace(/^(\d{2})(\d)/, '$1.$2');
    value = value.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
    value = value.replace(/\.(\d{3})(\d)/, '.$1/$2');
    value = value.replace(/(\d{4})(\d)/, '$1-$2');
    e.target.value = value;
});

// Validação final do formulário
document.querySelector('form').addEventListener('submit', function (e) {
    e.preventDefault();

    const nome = document.getElementById('nome_gestor').value.trim();
    const cpf = document.getElementById('cpf_gestor').value;
    const email = document.getElementById('email_gestor').value.trim();
    const razao = document.getElementById('razao_social').value.trim();
    const cnpj = document.getElementById('cnpj_instituicao').value;
    const senha = document.getElementById('senha').value;

    if (!nome || !cpf || !email || !razao || !cnpj || !senha) {
        alert('Por favor, preencha todos os campos obrigatórios.');
        return;
    }

    alert('Cadastro de Gestor realizado com sucesso!');
});
