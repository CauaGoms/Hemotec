let cadastroStep = 1;
const cadastroTotalSteps = 5;

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

    // Limpar erros anteriores
    currentSection.querySelectorAll('.is-invalid').forEach(field => {
        field.classList.remove('is-invalid');
    });

    let hasError = false;

    for (let field of requiredFields) {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            showFieldError(field, 'Este campo é obrigatório.');
            hasError = true;
        }
    }

    // Validações específicas por seção
    if (cadastroStep === 1) {
        // Validar nome
        const nome = document.getElementById('nome_gestor');
        if (nome.value.trim().length < 3) {
            showFieldError(nome, 'O nome deve ter pelo menos 3 caracteres.');
            hasError = true;
        }

        // Validar CPF
        const cpf = document.getElementById('cpf_gestor');
        if (!validarCPF(cpf.value)) {
            showFieldError(cpf, 'CPF inválido.');
            hasError = true;
        }

        // Validar email
        const email = document.getElementById('email_gestor');
        if (!validarEmail(email.value)) {
            showFieldError(email, 'Email inválido.');
            hasError = true;
        }

        // Validar telefone (opcional, mas se preenchido deve ser válido)
        const telefone = document.getElementById('telefone_gestor');
        if (telefone.value.trim() && !validarTelefone(telefone.value)) {
            showFieldError(telefone, 'Telefone inválido. Use o formato (XX) XXXXX-XXXX.');
            hasError = true;
        }

        // Validar data de nascimento
        const dataNasc = document.getElementById('data_nascimento_gestor');
        if (!validarIdade(dataNasc.value)) {
            showFieldError(dataNasc, 'Você deve ter pelo menos 18 anos.');
            hasError = true;
        }

        // Validar gênero
        const genero = document.getElementById('genero_gestor');
        if (!genero.value) {
            showFieldError(genero, 'Selecione um gênero.');
            hasError = true;
        }
    }

    if (cadastroStep === 2) {
        // Validar razão social
        const razao = document.getElementById('razao_social');
        if (razao.value.trim().length < 3) {
            showFieldError(razao, 'A razão social deve ter pelo menos 3 caracteres.');
            hasError = true;
        }

        // Validar CNPJ
        const cnpj = document.getElementById('cnpj_instituicao');
        if (!validarCNPJ(cnpj.value)) {
            showFieldError(cnpj, 'CNPJ inválido.');
            hasError = true;
        }

        // Validar email institucional
        const emailInst = document.getElementById('email_institucional');
        if (!validarEmail(emailInst.value)) {
            showFieldError(emailInst, 'Email institucional inválido.');
            hasError = true;
        }

        // Validar telefone institucional (opcional)
        const telefoneInst = document.getElementById('telefone_instituicao');
        if (telefoneInst.value.trim() && !validarTelefone(telefoneInst.value)) {
            showFieldError(telefoneInst, 'Telefone institucional inválido.');
            hasError = true;
        }
    }

    if (cadastroStep === 3) {
        // Validar CEP instituição
        const cep = document.getElementById('cep_instituicao');
        if (!validarCEP(cep.value)) {
            showFieldError(cep, 'CEP inválido. Use o formato XXXXX-XXX.');
            hasError = true;
        }

        // Validar estado
        const estado = document.getElementById('estado_instituicao');
        if (estado.value.length !== 2) {
            showFieldError(estado, 'Estado deve ter 2 letras (UF).');
            hasError = true;
        }
    }

    if (cadastroStep === 4) {
        // Validar CEP gestor
        const cepGestor = document.getElementById('cep_gestor');
        if (!validarCEP(cepGestor.value)) {
            showFieldError(cepGestor, 'CEP inválido. Use o formato XXXXX-XXX.');
            hasError = true;
        }

        // Validar estado
        const estadoGestor = document.getElementById('estado_gestor');
        if (estadoGestor.value.length !== 2) {
            showFieldError(estadoGestor, 'Estado deve ter 2 letras (UF).');
            hasError = true;
        }
    }

    if (cadastroStep === 5) {
        const senha = document.getElementById('senha');
        const confirmar = document.getElementById('confirmar_senha');

        // Validar senha
        if (!validarSenha(senha.value)) {
            showFieldError(senha, 'A senha deve ter pelo menos 6 caracteres, incluindo números e letras.');
            hasError = true;
        }

        // Validar confirmação
        if (senha.value !== confirmar.value) {
            showFieldError(confirmar, 'As senhas não coincidem.');
            hasError = true;
        }
    }

    if (hasError) {
        const firstInvalid = currentSection.querySelector('.is-invalid');
        if (firstInvalid) {
            firstInvalid.focus();
        }
    }

    return !hasError;
}

// Funções auxiliares de validação
function showFieldError(field, message) {
    field.classList.add('is-invalid');
    let feedback = field.parentElement.querySelector('.invalid-feedback');
    if (!feedback) {
        feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        field.parentElement.appendChild(feedback);
    }
    feedback.textContent = message;
    feedback.style.display = 'block';
}

function validarCPF(cpf) {
    cpf = cpf.replace(/\D/g, '');
    if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)) return false;

    let soma = 0;
    let resto;

    for (let i = 1; i <= 9; i++) {
        soma += parseInt(cpf.substring(i - 1, i)) * (11 - i);
    }
    resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpf.substring(9, 10))) return false;

    soma = 0;
    for (let i = 1; i <= 10; i++) {
        soma += parseInt(cpf.substring(i - 1, i)) * (12 - i);
    }
    resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpf.substring(10, 11))) return false;

    return true;
}

function validarCNPJ(cnpj) {
    cnpj = cnpj.replace(/\D/g, '');
    if (cnpj.length !== 14 || /^(\d)\1+$/.test(cnpj)) return false;

    let tamanho = cnpj.length - 2;
    let numeros = cnpj.substring(0, tamanho);
    let digitos = cnpj.substring(tamanho);
    let soma = 0;
    let pos = tamanho - 7;

    for (let i = tamanho; i >= 1; i--) {
        soma += numeros.charAt(tamanho - i) * pos--;
        if (pos < 2) pos = 9;
    }

    let resultado = soma % 11 < 2 ? 0 : 11 - (soma % 11);
    if (resultado != digitos.charAt(0)) return false;

    tamanho = tamanho + 1;
    numeros = cnpj.substring(0, tamanho);
    soma = 0;
    pos = tamanho - 7;

    for (let i = tamanho; i >= 1; i--) {
        soma += numeros.charAt(tamanho - i) * pos--;
        if (pos < 2) pos = 9;
    }

    resultado = soma % 11 < 2 ? 0 : 11 - (soma % 11);
    if (resultado != digitos.charAt(1)) return false;

    return true;
}

function validarEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validarTelefone(telefone) {
    const digits = telefone.replace(/\D/g, '');
    return digits.length === 10 || digits.length === 11;
}

function validarCEP(cep) {
    const digits = cep.replace(/\D/g, '');
    return digits.length === 8;
}

function validarIdade(dataNascimento) {
    if (!dataNascimento) return false;
    const hoje = new Date();
    const nascimento = new Date(dataNascimento);
    let idade = hoje.getFullYear() - nascimento.getFullYear();
    const mes = hoje.getMonth() - nascimento.getMonth();
    if (mes < 0 || (mes === 0 && hoje.getDate() < nascimento.getDate())) {
        idade--;
    }
    return idade >= 18;
}

function validarSenha(senha) {
    if (senha.length < 6) return false;
    const temNumero = /\d/.test(senha);
    const temLetra = /[a-zA-Z]/.test(senha);
    return temNumero && temLetra;
}

// Máscara simples para CPF do gestor
document.getElementById('cpf_gestor').addEventListener('input', function (e) {
    let value = e.target.value.replace(/\D/g, '');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    e.target.value = value;
});

// Máscara para telefone do gestor
document.getElementById('telefone_gestor').addEventListener('input', function (e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length <= 2) {
        e.target.value = value ? `(${value}` : '';
    } else if (value.length <= 6) {
        e.target.value = `(${value.slice(0, 2)}) ${value.slice(2)}`;
    } else if (value.length <= 10) {
        e.target.value = `(${value.slice(0, 2)}) ${value.slice(2, 6)}-${value.slice(6)}`;
    } else {
        e.target.value = `(${value.slice(0, 2)}) ${value.slice(2, 7)}-${value.slice(7, 11)}`;
    }
});

// Formatar telefone_gestor inicial (se preenchido pelo servidor sem máscara)
document.addEventListener('DOMContentLoaded', function () {
    const telEl = document.getElementById('telefone_gestor');
    if (telEl && telEl.value) {
        let digits = telEl.value.replace(/\D/g, '');
        if (digits.length > 0) {
            if (digits.length <= 2) {
                telEl.value = `(${digits}`;
            } else if (digits.length <= 6) {
                telEl.value = `(${digits.slice(0, 2)}) ${digits.slice(2)}`;
            } else if (digits.length <= 10) {
                telEl.value = `(${digits.slice(0, 2)}) ${digits.slice(2, 6)}-${digits.slice(6)}`;
            } else {
                telEl.value = `(${digits.slice(0, 2)}) ${digits.slice(2, 7)}-${digits.slice(7, 11)}`;
            }
        }
    }
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

// Máscara para telefone da instituição
document.getElementById('telefone_instituicao').addEventListener('input', function (e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length <= 2) {
        e.target.value = value ? `(${value}` : '';
    } else if (value.length <= 6) {
        e.target.value = `(${value.slice(0, 2)}) ${value.slice(2)}`;
    } else if (value.length <= 10) {
        e.target.value = `(${value.slice(0, 2)}) ${value.slice(2, 6)}-${value.slice(6)}`;
    } else {
        e.target.value = `(${value.slice(0, 2)}) ${value.slice(2, 7)}-${value.slice(7, 11)}`;
    }
});

// Máscara para CEP do gestor
document.getElementById('cep_gestor').addEventListener('input', function (e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length <= 5) {
        e.target.value = value;
    } else {
        e.target.value = `${value.slice(0, 5)}-${value.slice(5, 8)}`;
    }
});

// Máscara para CEP da instituição
document.getElementById('cep_instituicao').addEventListener('input', function (e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length <= 5) {
        e.target.value = value;
    } else {
        e.target.value = `${value.slice(0, 5)}-${value.slice(5, 8)}`;
    }
});

// Remover erro quando o usuário começar a corrigir
document.addEventListener('DOMContentLoaded', function () {
    const allInputs = document.querySelectorAll('input, select');
    allInputs.forEach(input => {
        input.addEventListener('input', function () {
            if (this.classList.contains('is-invalid')) {
                this.classList.remove('is-invalid');
                const feedback = this.parentElement.querySelector('.invalid-feedback');
                if (feedback) {
                    feedback.style.display = 'none';
                }
            }
        });
    });
});

// Validação final do formulário
document.querySelector('form').addEventListener('submit', function (e) {
    // Validar todos os steps antes do envio
    let formValid = true;

    // Salvar step atual
    const currentStep = cadastroStep;

    // Validar cada step
    for (let step = 1; step <= cadastroTotalSteps; step++) {
        cadastroStep = step;
        if (!cadastroValidateCurrentStep()) {
            formValid = false;
            // Voltar para o primeiro step com erro
            if (step < currentStep) {
                document.getElementById(`cadastroSection${currentStep}`).style.display = 'none';
                document.getElementById(`cadastroSection${step}`).style.display = 'block';
                cadastroUpdateButtons();
            }
            break;
        }
    }

    // Restaurar step original
    cadastroStep = currentStep;

    if (!formValid) {
        e.preventDefault();
        if (window.showWarning) window.showWarning('Por favor, corrija os erros no formulário.');
        return false;
    }

    // Formulário válido - deixar enviar
    return true;
});

// Preenchimento automático de endereço pelo CEP da instituição
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
                    document.getElementById('estado_instituicao').value = data.uf || '';
                } else {
                    document.getElementById('rua_instituicao').value = '';
                    document.getElementById('bairro_instituicao').value = '';
                    document.getElementById('cidade_instituicao').value = '';
                    document.getElementById('estado_instituicao').value = '';
                    if (window.showWarning) window.showWarning('CEP não encontrado.');
                }
            })
            .catch(() => {
                if (window.showError) window.showError('Erro ao buscar o CEP.');
            });
    }
});

// Preenchimento automático de endereço pelo CEP do gestor
document.getElementById('cep_gestor').addEventListener('blur', function (e) {
    const cep = e.target.value.replace(/\D/g, '');
    if (cep.length === 8) {
        fetch(`https://viacep.com.br/ws/${cep}/json/`)
            .then(response => response.json())
            .then(data => {
                if (!data.erro) {
                    document.getElementById('rua_gestor').value = data.logradouro || '';
                    document.getElementById('bairro_gestor').value = data.bairro || '';
                    document.getElementById('cidade_gestor').value = data.localidade || '';
                    document.getElementById('estado_gestor').value = data.uf || '';
                } else {
                    document.getElementById('rua_gestor').value = '';
                    document.getElementById('bairro_gestor').value = '';
                    document.getElementById('cidade_gestor').value = '';
                    document.getElementById('estado_gestor').value = '';
                    if (window.showWarning) window.showWarning('CEP não encontrado.');
                }
            })
            .catch(() => {
                if (window.showError) window.showError('Erro ao buscar o CEP.');
            });
    }
});
