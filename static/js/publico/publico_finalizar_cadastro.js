let cadastroStep = 1;
const cadastroTotalSteps = 4;

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

    if (cadastroStep === 4) {
        const senha = document.getElementById('senha').value;
        const confirmar = document.getElementById('confirmar_senha').value;
        if (senha !== confirmar) {
            const confirmField = document.getElementById('confirmar_senha');
            if (confirmField) {
                confirmField.classList.add('is-invalid');
                let fb = confirmField.parentElement.querySelector('.invalid-feedback');
                if (!fb) { fb = document.createElement('div'); fb.className = 'invalid-feedback'; confirmField.parentElement.appendChild(fb); }
                fb.textContent = 'As senhas não coincidem';
            }
            if (window.showError) window.showError('As senhas não coincidem!');
            return false;
        }
        if (senha.length < 6) {
            const senhaField = document.getElementById('senha');
            if (senhaField) {
                senhaField.classList.add('is-invalid');
                let fb = senhaField.parentElement.querySelector('.invalid-feedback');
                if (!fb) { fb = document.createElement('div'); fb.className = 'invalid-feedback'; senhaField.parentElement.appendChild(fb); }
                fb.textContent = 'A senha deve ter pelo menos 6 caracteres.';
            }
            if (window.showWarning) window.showWarning('A senha deve ter pelo menos 6 caracteres.');
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
        if (window.showWarning) window.showWarning('Por favor, preencha todos os campos obrigatórios.');
        return;
    }

    if (document && document.querySelector('form')) {
        document.querySelector('form').submit();
    }
});

// Preenchimento automático de endereço pelo CEP
document.getElementById('cep_instituicao').addEventListener('blur', function (e) {
    const cep = e.target.value.replace(/\D/g, '');
    if (cep.length === 8) {
        fetch(`https://viacep.com.br/ws/${cep}/json/`)
            .then(response => response.json())
            .then(data => {
                if (!data.erro) {
                    document.getElementById('rua_instituicao').value = data.logradouro || '';
                    document.getElementById('bairro_instituicao').value = data.bairro || '';
                    document.getElementById('cidade_instituicao').value = data.localidade || '';
                } else {
                    document.getElementById('rua_instituicao').value = '';
                    document.getElementById('bairro_instituicao').value = '';
                    document.getElementById('cidade_instituicao').value = '';
                    if (window.showWarning) window.showWarning('CEP não encontrado.');
                }
            })
            .catch(() => {
                if (window.showError) window.showError('Erro ao buscar o CEP.');
            });
    }
});
