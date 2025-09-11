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

    // Deixa o botão Próximo menor só na segunda seção (cadastroStep === 2)
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
    // Validação extra para senha
    if (cadastroStep === 3) {
        const senha = document.getElementById('senha').value;
        const confirmar = document.getElementById('confirmarSenha').value;
        if (senha !== confirmar) {
            alert('As senhas não coincidem!');
            return false;
        }
    }
    return true;
}
document.getElementById('cpf').addEventListener('input', function (e) {
    let value = e.target.value.replace(/\D/g, '');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    e.target.value = value;
});

// Máscara para CEP
document.getElementById('cep').addEventListener('input', function (e) {
    let value = e.target.value.replace(/\D/g, '');
    value = value.replace(/(\d{5})(\d)/, '$1-$2');
    e.target.value = value;
});

// Função para mostrar loading no campo CEP
function showCepLoading(show) {
    const cepField = document.getElementById('cep');
    if (show) {
        cepField.style.backgroundImage = 'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'20\' height=\'20\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'%23e02020\' stroke-width=\'2\' stroke-linecap=\'round\' stroke-linejoin=\'round\'%3E%3Cpath d=\'M21 12a9 9 0 11-6.219-8.56\'/%3E%3C/svg%3E")';
        cepField.style.backgroundRepeat = 'no-repeat';
        cepField.style.backgroundPosition = 'right 15px center';
        cepField.style.backgroundSize = '20px';
        // cepField.style.animation = 'spin 1s linear infinite';
    } else {
        cepField.style.backgroundImage = 'none';
        cepField.style.animation = 'none';
    }
}

// Função para animar campos preenchidos
function animateFilledField(fieldId) {
    const field = document.getElementById(fieldId);
    field.classList.add('auto-filled');
    setTimeout(() => {
        field.classList.remove('auto-filled');
    }, 1000);
}

// Função para buscar endereço pelo CEP
document.getElementById('cep').addEventListener('blur', function () {
    const cep = this.value.replace(/\D/g, '');

    if (cep.length === 8) {
        showCepLoading(true);

        // Limpa os campos antes de preencher
        const ruaField = document.getElementById('rua');
        const bairroField = document.getElementById('bairro');
        const cidadeField = document.getElementById('cidade');

        ruaField.value = '';
        bairroField.value = '';
        cidadeField.value = '';

        // Faz a requisição para a API ViaCEP
        fetch(`https://viacep.com.br/ws/${cep}/json/`)
            .then(response => response.json())
            .then(data => {
                showCepLoading(false);
                if (!data.erro) {
                    if (data.logradouro) {
                        ruaField.value = data.logradouro;
                        animateFilledField('rua');
                    }
                    if (data.bairro) {
                        bairroField.value = data.bairro;
                        animateFilledField('bairro');
                    }
                    if (data.localidade) {
                        cidadeField.value = data.localidade;
                        animateFilledField('cidade');
                    }
                    // Preenche o campo UF
                    var ufField = document.getElementById('uf');
                    if (data.uf && ufField) {
                        ufField.value = data.uf;
                        animateFilledField('uf');
                    }
                    if (!data.logradouro) {
                        ruaField.focus();
                    }
                } else {
                    this.style.borderColor = '#dc3545';
                    alert('CEP não encontrado! Verifique o número digitado.');
                    setTimeout(() => {
                        this.style.borderColor = '#ced4da';
                    }, 3000);
                }
            })
            .catch(error => {
                showCepLoading(false);
                console.error('Erro ao buscar CEP:', error);
                this.style.borderColor = '#dc3545';
                alert('Erro ao buscar CEP. Verifique sua conexão e tente novamente.');
                setTimeout(() => {
                    this.style.borderColor = '#ced4da';
                }, 3000);
            });
    } else if (cep.length > 0) {
        this.style.borderColor = '#dc3545';
        setTimeout(() => {
            this.style.borderColor = '#ced4da';
        }, 3000);
    }
});

// Validação de CPF
function validarCPF(cpf) {
    cpf = cpf.replace(/\D/g, '');
    if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) return false;

    let soma = 0;
    for (let i = 0; i < 9; i++) {
        soma += parseInt(cpf.charAt(i)) * (10 - i);
    }
    let resto = 11 - (soma % 11);
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpf.charAt(9))) return false;

    soma = 0;
    for (let i = 0; i < 10; i++) {
        soma += parseInt(cpf.charAt(i)) * (11 - i);
    }
    resto = 11 - (soma % 11);
    if (resto === 10 || resto === 11) resto = 0;
    return resto === parseInt(cpf.charAt(10));
}

// Validação do formulário
document.getElementById('cadastroForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const cpf = document.getElementById('cpf').value;
    const birthdate = document.getElementById('birthdate').value;
    const cep = document.getElementById('cep').value;
    const rua = document.getElementById('rua').value.trim();
    const bairro = document.getElementById('bairro').value.trim();
    const cidade = document.getElementById('cidade').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    // Validações
    if (!name) {
        alert('Por favor, preencha seu nome completo.');
        document.getElementById('name').focus();
        return;
    }

    if (!email) {
        alert('Por favor, preencha seu e-mail.');
        document.getElementById('email').focus();
        return;
    }

    if (!validarCPF(cpf)) {
        alert('CPF inválido! Verifique os números digitados.');
        document.getElementById('cpf').focus();
        return;
    }

    if (!birthdate) {
        alert('Por favor, informe sua data de nascimento.');
        document.getElementById('birthdate').focus();
        return;
    }

    if (cep.replace(/\D/g, '').length !== 8) {
        alert('CEP inválido! Digite um CEP válido.');
        document.getElementById('cep').focus();
        return;
    }

    if (!rua || !bairro || !cidade) {
        alert('Por favor, preencha todos os campos de endereço.');
        return;
    }

    if (password.length < 6) {
        alert('A senha deve ter pelo menos 6 caracteres.');
        document.getElementById('password').focus();
        return;
    }

    if (password !== confirmPassword) {
        alert('As senhas não coincidem!');
        document.getElementById('confirm-password').focus();
        return;
    }

    // Aqui você pode adicionar a lógica para enviar os dados
    alert('Cadastro realizado com sucesso!');
});

// Adiciona animação de loading CSS
const style = document.createElement('style');
style.textContent = `
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        `;
document.head.appendChild(style);