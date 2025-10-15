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
    
    // Validação do campo gênero na Seção 1
    if (cadastroStep === 1) {
        const generoEl = document.getElementById('genero');
        if (generoEl && !generoEl.value) {
            generoEl.classList.add('is-invalid');
            generoEl.focus();
            if (window.showWarning) window.showWarning('Por favor, selecione o gênero');
            return false;
        } else if (generoEl) {
            generoEl.classList.remove('is-invalid');
        }
    }
    
    // Validação extra para senha
    if (cadastroStep === 3) {
        const senhaEl = document.getElementById('password');
        const confirmarEl = document.getElementById('confirm-password');
        const senha = senhaEl ? senhaEl.value : '';
        const confirmar = confirmarEl ? confirmarEl.value : '';
        // Regras de senha forte no cliente
        const pwdRules = {
            min: 8,
            upper: /[A-Z]/,
            lower: /[a-z]/,
            digit: /\d/,
            symbol: /[^A-Za-z0-9]/
        };
        const common = ['123456', '12345678', '123456789', 'password', 'senha', 'senha123', 'admin', 'abcd1234', 'qwerty', '111111'];

        if (senha.length < pwdRules.min || !pwdRules.upper.test(senha) || !pwdRules.lower.test(senha) || !pwdRules.digit.test(senha) || !pwdRules.symbol.test(senha) || common.includes(senha.toLowerCase())) {
            if (senhaEl) markInvalid(senhaEl, 'Senha fraca. Use ≥8 chars, 1 maiúscula, 1 minúscula, 1 número e 1 símbolo.');
            if (window.showWarning) window.showWarning('Senha fraca. Use pelo menos 8 caracteres, incluindo maiúscula, minúscula, número e símbolo.');
            if (senhaEl) senhaEl.focus();
            return false;
        }

        if (senha !== confirmar) {
            // feedback inline + toast
            if (confirmarEl) markInvalid(confirmarEl, 'As senhas não coincidem');
            if (window.showError) window.showError('As senhas não coincidem');
            return false;
        }
    }
    return true;
}

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
// Inicialização segura quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function () {
    // Máscara CPF
    const cpfEl = document.getElementById('cpf');
    if (cpfEl) {
        cpfEl.addEventListener('input', function (e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
            e.target.value = value;
        });
    }

    // Máscara CEP
    const cepEl = document.getElementById('cep');
    if (cepEl) {
        cepEl.addEventListener('input', function (e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{5})(\d)/, '$1-$2');
            e.target.value = value;
        });

        // Busca endereço ao perder foco
        cepEl.addEventListener('blur', function () {
            const self = this;
            const cep = self.value.replace(/\D/g, '');

            if (cep.length === 8) {
                showCepLoading(true);

                // Limpa os campos antes de preencher
                const ruaField = document.getElementById('rua');
                const bairroField = document.getElementById('bairro');
                const cidadeField = document.getElementById('cidade');

                if (ruaField) ruaField.value = '';
                if (bairroField) bairroField.value = '';
                if (cidadeField) cidadeField.value = '';

                fetch(`https://viacep.com.br/ws/${cep}/json/`)
                    .then(response => response.json())
                    .then(data => {
                        showCepLoading(false);
                        if (!data.erro) {
                            if (data.logradouro && ruaField) {
                                ruaField.value = data.logradouro;
                                animateFilledField('rua');
                            }
                            if (data.bairro && bairroField) {
                                bairroField.value = data.bairro;
                                animateFilledField('bairro');
                            }
                            if (data.localidade && cidadeField) {
                                cidadeField.value = data.localidade;
                                animateFilledField('cidade');
                            }
                            // Preenche o campo UF
                            var ufField = document.getElementById('uf');
                            if (data.uf && ufField) {
                                ufField.value = data.uf;
                                animateFilledField('uf');
                            }
                            if (!data.logradouro && ruaField) {
                                ruaField.focus();
                            }
                        } else {
                            self.style.borderColor = '#dc3545';
                            if (window.showWarning) window.showWarning('CEP não encontrado! Verifique o número digitado.');
                            if (cepEl) markInvalid(cepEl, 'CEP não encontrado');
                            setTimeout(() => {
                                self.style.borderColor = '#ced4da';
                                if (cepEl) clearInvalid(cepEl);
                            }, 3000);
                        }
                    })
                    .catch(error => {
                        showCepLoading(false);
                        console.error('Erro ao buscar CEP:', error);
                        self.style.borderColor = '#dc3545';
                        if (window.showError) window.showError('Erro ao buscar CEP. Verifique sua conexão e tente novamente.');
                        if (cepEl) markInvalid(cepEl, 'Erro ao buscar CEP');
                        setTimeout(() => {
                            self.style.borderColor = '#ced4da';
                            if (cepEl) clearInvalid(cepEl);
                        }, 3000);
                    });
            } else if (cep.length > 0) {
                self.style.borderColor = '#dc3545';
                setTimeout(() => {
                    self.style.borderColor = '#ced4da';
                }, 3000);
            }
        });
    }

    // Telefone: manter raw digits em dataset e aplicar máscara de exibição (ex: (28) 99933-3417)
    const telefoneEl = document.getElementById('telefone');
    function formatPhone(digits) {
        if (!digits) return '';
        const d = digits.slice(0, 11);
        if (d.length <= 2) return `(${d}`;
        if (d.length <= 6) return `(${d.slice(0, 2)}) ${d.slice(2)}`;
        if (d.length <= 10) return `(${d.slice(0, 2)}) ${d.slice(2, 6)}-${d.slice(6)}`;
        // 11 digits
        return `(${d.slice(0, 2)}) ${d.slice(2, 7)}-${d.slice(7, 11)}`;
    }
    if (telefoneEl) {
        // garantir maxlength suficiente para a máscara (ex: '(11) 99999-9999' -> 15 chars)
        try { telefoneEl.maxLength = 15; } catch (e) { }
        // inicializar dataset.raw com value existente (apenas dígitos)
        telefoneEl.dataset.raw = (telefoneEl.value || '').replace(/\D/g, '').slice(0, 11);
        telefoneEl.value = formatPhone(telefoneEl.dataset.raw);

        telefoneEl.addEventListener('input', function (e) {
            // extrair dígitos do valor atual (pode conter máscara)
            const onlyDigits = e.target.value.replace(/\D/g, '').slice(0, 11);
            e.target.dataset.raw = onlyDigits;
            e.target.value = formatPhone(onlyDigits);
        });

        telefoneEl.addEventListener('paste', function (e) {
            e.preventDefault();
            const paste = (e.clipboardData || window.clipboardData).getData('text') || '';
            const onlyDigits = paste.replace(/\D/g, '').slice(0, 11);
            // substituir seleção atual pelo pasted digits
            const start = this.selectionStart || 0;
            const end = this.selectionEnd || 0;
            const currentDigits = (this.dataset.raw || '').toString();
            const newDigits = (currentDigits.slice(0, start) + onlyDigits + currentDigits.slice(end)).replace(/\D/g, '').slice(0, 11);
            this.dataset.raw = newDigits;
            this.value = formatPhone(newDigits);
        });
    }

    // Validação do formulário (evento submit)
    const form = document.getElementById('cadastroForm') || document.querySelector('form[action="/cadastrar"]');
    if (form) {
        // Desativa a validação nativa do navegador para controlar via JS
        try { form.noValidate = true; } catch (e) { /* ignore */ }
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const nameEl = document.getElementById('name');
            const emailEl = document.getElementById('email');
            const cpfEl2 = document.getElementById('cpf');
            const birthdateEl = document.getElementById('birthdate');
            const cepEl2 = document.getElementById('cep');
            const ruaEl = document.getElementById('rua');
            const bairroEl = document.getElementById('bairro');
            const cidadeEl = document.getElementById('cidade');
            const passwordEl = document.getElementById('password');
            const confirmEl = document.getElementById('confirm-password');

            const name = nameEl ? nameEl.value.trim() : '';
            const email = emailEl ? emailEl.value.trim() : '';
            const cpf = cpfEl2 ? cpfEl2.value : '';
            const birthdate = birthdateEl ? birthdateEl.value : '';
            const cep = cepEl2 ? cepEl2.value : '';
            const rua = ruaEl ? ruaEl.value.trim() : '';
            const bairro = bairroEl ? bairroEl.value.trim() : '';
            const cidade = cidadeEl ? cidadeEl.value.trim() : '';
            const password = passwordEl ? passwordEl.value : '';
            const confirmPassword = confirmEl ? confirmEl.value : '';

            // Validações (feedback inline + toasts)
            if (!name) {
                if (nameEl) markInvalid(nameEl, 'Por favor, preencha seu nome completo.');
                if (window.showWarning) window.showWarning('Por favor, preencha seu nome completo.');
                if (nameEl) nameEl.focus();
                return;
            } else if (nameEl) clearInvalid(nameEl);

            if (!email) {
                if (emailEl) markInvalid(emailEl, 'Por favor, preencha seu e-mail.');
                if (window.showWarning) window.showWarning('Por favor, preencha seu e-mail.');
                if (emailEl) emailEl.focus();
                return;
            } else if (emailEl) clearInvalid(emailEl);

            // Validação de formato do email (evita depender da validação nativa do browser)
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (email && !emailRegex.test(email)) {
                if (emailEl) markInvalid(emailEl, 'E-mail inválido');
                if (window.showWarning) window.showWarning('E-mail inválido. Verifique o formato.');
                // foco seguro
                if (emailEl) {
                    try {
                        const hidden = emailEl.disabled || emailEl.offsetParent === null;
                        if (!hidden && typeof emailEl.focus === 'function') emailEl.focus();
                        else emailEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    } catch (ex) {
                        try { emailEl.scrollIntoView({ behavior: 'smooth', block: 'center' }); } catch (_) { }
                    }
                }
                return;
            } else if (emailEl) clearInvalid(emailEl);

            if (!validarCPF(cpf)) {
                if (cpfEl2) markInvalid(cpfEl2, 'CPF inválido');
                if (window.showError) window.showError('CPF inválido! Verifique os números digitados.');
                if (cpfEl2) cpfEl2.focus();
                return;
            } else if (cpfEl2) clearInvalid(cpfEl2);

            if (!birthdate) {
                if (birthdateEl) markInvalid(birthdateEl, 'Informe sua data de nascimento');
                if (window.showWarning) window.showWarning('Por favor, informe sua data de nascimento.');
                if (birthdateEl) birthdateEl.focus();
                return;
            } else if (birthdateEl) clearInvalid(birthdateEl);

            if (!cepEl2 || cep.replace(/\D/g, '').length !== 8) {
                if (cepEl2) markInvalid(cepEl2, 'CEP inválido');
                if (window.showWarning) window.showWarning('CEP inválido! Digite um CEP válido.');
                if (cepEl2) cepEl2.focus();
                return;
            } else if (cepEl2) clearInvalid(cepEl2);

            // Validação do telefone: apenas dígitos e 10 ou 11 caracteres (DDD + número)
            const telefoneDigits = (telefoneEl && telefoneEl.dataset && telefoneEl.dataset.raw) ? telefoneEl.dataset.raw.replace(/\D/g, '') : '';
            if (!telefoneDigits || (telefoneDigits.length !== 10 && telefoneDigits.length !== 11)) {
                if (telefoneEl) markInvalid(telefoneEl, 'Telefone deve conter 10 ou 11 dígitos');
                if (window.showWarning) window.showWarning('Telefone inválido. Informe DDD + número (10 ou 11 dígitos).');
                if (telefoneEl) {
                    try {
                        const hidden = telefoneEl.disabled || telefoneEl.offsetParent === null;
                        if (!hidden && typeof telefoneEl.focus === 'function') telefoneEl.focus();
                        else telefoneEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    } catch (ex) { try { telefoneEl.scrollIntoView({ behavior: 'smooth', block: 'center' }); } catch (_) { } }
                }
                return;
            } else if (telefoneEl) clearInvalid(telefoneEl);

            if (!rua || !bairro || !cidade) {
                if (window.showWarning) window.showWarning('Por favor, preencha todos os campos de endereço.');
                return;
            }

            // Validação forte de senha no cliente
            const pwdMin = 8;
            const hasUpper = /[A-Z]/.test(password);
            const hasLower = /[a-z]/.test(password);
            const hasDigit = /\d/.test(password);
            const hasSymbol = /[^A-Za-z0-9]/.test(password);
            const blacklist = ['123456', '12345678', '123456789', 'password', 'senha', 'senha123', 'admin', 'abcd1234', 'qwerty', '111111'];

            if (password.length < pwdMin || !hasUpper || !hasLower || !hasDigit || !hasSymbol || blacklist.includes(password.toLowerCase())) {
                if (passwordEl) markInvalid(passwordEl, 'Senha inválida: mínimo 8 caracteres, 1 maiúscula, 1 minúscula, 1 número e 1 símbolo; evite senhas comuns.');
                if (window.showWarning) window.showWarning('Senha inválida. Verifique os requisitos de complexidade.');
                if (passwordEl) passwordEl.focus();
                return;
            } else if (passwordEl) clearInvalid(passwordEl);

            if (password !== confirmPassword) {
                if (confirmEl) markInvalid(confirmEl, 'As senhas não coincidem');
                if (window.showError) window.showError('As senhas não coincidem!');
                if (confirmEl) confirmEl.focus();
                return;
            } else if (confirmEl) clearInvalid(confirmEl);

            // Submeter o formulário ao servidor (validação do servidor também ocorrerá lá)
            if (form) {
                // Submete o formulário programaticamente (form.submit() não dispara o event listener novamente)
                form.submit();
            }
        });
    }

    // Toggle para mostrar/ocultar senhas
    document.querySelectorAll('.btn-toggle-password').forEach(btn => {
        // tornar a 'caixinha' do olhinho menor/mais compacta via estilos inline
        try {
            btn.style.padding = '0 0.5rem';
            btn.style.minWidth = '33px';
            btn.style.height = '51px';
            btn.style.borderRadius = '0 28px 28px 0';
            btn.style.display = 'flex';
            btn.style.alignItems = 'center';
            btn.style.justifyContent = 'center';
            const ic = btn.querySelector('i');
            if (ic) ic.style.fontSize = '0.95rem';
        } catch (e) {
            // ignore style failures
        }

        btn.addEventListener('click', function () {
            const targetId = this.getAttribute('data-target');
            const input = document.getElementById(targetId);
            if (!input) return;
            const icon = this.querySelector('i');
            if (input.type === 'password') {
                input.type = 'text';
                if (icon) {
                    icon.classList.remove('fa-eye');
                    icon.classList.add('fa-eye-slash');
                }
                this.setAttribute('aria-label', 'Ocultar senha');
            } else {
                input.type = 'password';
                if (icon) {
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                }
                this.setAttribute('aria-label', 'Mostrar senha');
            }
        });
    });
});

// Validação de senha em tempo real
function validatePasswordRealtime() {
    const pwdEl = document.getElementById('password');
    const confEl = document.getElementById('confirm-password');
    if (!pwdEl) return;

    const check = () => {
        const pwd = pwdEl.value || '';
        const conf = confEl ? confEl.value || '' : '';
        const pwdMin = 8;
        const hasUpper = /[A-Z]/.test(pwd);
        const hasLower = /[a-z]/.test(pwd);
        const hasDigit = /\d/.test(pwd);
        const hasSymbol = /[^A-Za-z0-9]/.test(pwd);
        const blacklist = ['123456', '12345678', '123456789', 'password', 'senha', 'senha123', 'admin', 'abcd1234', 'qwerty', '111111'];

        // senha fraca
        if (pwd.length > 0 && (pwd.length < pwdMin || !hasUpper || !hasLower || !hasDigit || !hasSymbol || blacklist.includes(pwd.toLowerCase()))) {
            markInvalid(pwdEl, 'Senha fraca. Sua senha deve ter no mínimo 8 caracteres, 1 maiúscula, 1 minúscula, 1 número e 1 símbolo');
        } else {
            clearInvalid(pwdEl);
        }

        // confirmação
        if (confEl && conf.length > 0) {
            if (pwd !== conf) {
                markInvalid(confEl, 'As senhas não coincidem');
            } else {
                clearInvalid(confEl);
            }
        }
    };

    pwdEl.addEventListener('input', check);
    if (confEl) confEl.addEventListener('input', check);
}

// Inicializa validação em tempo real quando o script carregar
try { validatePasswordRealtime(); } catch (e) { /* ignore */ }

// Helper: marcar campo como inválido e mostrar mensagem inline
function markInvalid(field, message) {
    try {
        field.classList.add('is-invalid');
        // procurar ou criar .invalid-feedback
        let fb = field.parentElement.querySelector('.invalid-feedback');
        if (!fb) {
            fb = document.createElement('div');
            fb.className = 'invalid-feedback';
            field.parentElement.appendChild(fb);
        }
        fb.textContent = message;
    } catch (e) {
        console.warn('markInvalid error', e);
    }
}

function clearInvalid(field) {
    try {
        field.classList.remove('is-invalid');
        const fb = field.parentElement.querySelector('.invalid-feedback');
        if (fb) fb.textContent = '';
    } catch (e) {
        console.warn('clearInvalid error', e);
    }
}

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

// Adiciona animação de loading CSS
const style = document.createElement('style');
style.textContent = `
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        `;
document.head.appendChild(style);