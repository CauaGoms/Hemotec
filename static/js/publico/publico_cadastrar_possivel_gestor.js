// JS para navegação entre etapas do formulário multi-step

// Função para validar e ir para a próxima página (escopo global)
window.validarEProximo = function () {
    const nomeEl = document.getElementById('nome');
    const cargoEl = document.getElementById('cargo');
    const emailEl = document.getElementById('email');
    const telefoneEl = document.getElementById('telefone');

    const nome = nomeEl ? nomeEl.value.trim() : '';
    const cargo = cargoEl ? cargoEl.value : '';
    const email = emailEl ? emailEl.value.trim() : '';
    const telefone = telefoneEl ? telefoneEl.value.trim() : '';

    let valid = true;

    // Validação do nome - mínimo 3 caracteres
    if (!nome) {
        markInvalid(nomeEl, 'Por favor, preencha seu nome completo.');
        if (window.showWarning) window.showWarning('Por favor, preencha seu nome completo.');
        nomeEl.focus();
        valid = false;
    } else if (nome.length < 3) {
        markInvalid(nomeEl, 'O nome deve ter no mínimo 3 caracteres.');
        if (window.showWarning) window.showWarning('O nome deve ter no mínimo 3 caracteres.');
        nomeEl.focus();
        valid = false;
    } else {
        clearInvalid(nomeEl);
    }

    if (!valid) return;

    // Validação do cargo
    if (!cargo || cargo === '') {
        markInvalid(cargoEl, 'Por favor, selecione seu cargo.');
        if (window.showWarning) window.showWarning('Por favor, selecione seu cargo.');
        cargoEl.focus();
        valid = false;
    } else {
        clearInvalid(cargoEl);
    }

    if (!valid) return;

    // Validação do email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email) {
        markInvalid(emailEl, 'Por favor, preencha seu e-mail.');
        if (window.showWarning) window.showWarning('Por favor, preencha seu e-mail.');
        emailEl.focus();
        valid = false;
    } else if (!emailRegex.test(email)) {
        markInvalid(emailEl, 'E-mail inválido.');
        if (window.showWarning) window.showWarning('E-mail inválido. Verifique o formato.');
        emailEl.focus();
        valid = false;
    } else {
        clearInvalid(emailEl);
    }

    if (!valid) return;

    // Validação do telefone
    const telefoneDigits = telefone.replace(/\D/g, '');
    if (!telefone) {
        markInvalid(telefoneEl, 'Por favor, preencha seu telefone.');
        if (window.showWarning) window.showWarning('Por favor, preencha seu telefone.');
        telefoneEl.focus();
        valid = false;
    } else if (telefoneDigits.length !== 10 && telefoneDigits.length !== 11) {
        markInvalid(telefoneEl, 'Telefone deve conter 10 ou 11 dígitos (DDD + número).');
        if (window.showWarning) window.showWarning('Telefone inválido. Informe DDD + número (10 ou 11 dígitos).');
        telefoneEl.focus();
        valid = false;
    } else {
        clearInvalid(telefoneEl);
    }

    if (!valid) return;

    // Se todas as validações passarem, enviar via AJAX para o servidor
    const formData = new FormData();
    formData.append('nome', nome);
    formData.append('cargo', cargo);
    formData.append('email', email);
    // Enviar apenas dígitos para o servidor
    const telefoneOnlyDigits = telefone.replace(/\D/g, '');
    formData.append('telefone', telefoneOnlyDigits);

    const btn = document.getElementById('btnProximo');
    if (btn) {
        const original = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Enviando...';
        btn.disabled = true;

        fetch('/cadastrar_possivel_gestor', {
            method: 'POST',
            body: formData,
        })
            .then(async res => {
                btn.innerHTML = original;
                btn.disabled = false;
                if (!res.ok) {
                    const data = await res.json().catch(() => ({}));
                    throw new Error(data.message || 'Erro ao enviar formulário');
                }
                return res.json();
            })
            .then(data => {
                // Se inserido com sucesso, redirecionar para finalizar cadastro com id
                if (data && data.success) {
                    const id = data.id;
                    window.location.href = `/finalizar_cadastro?possivel_id=${encodeURIComponent(id)}`;
                } else {
                    if (window.showWarning) window.showWarning(data.message || 'Erro ao enviar.');
                }
            })
            .catch(err => {
                console.error('Erro ao enviar possivel gestor:', err);
                if (window.showWarning) window.showWarning(err.message || 'Erro ao enviar formulário.');
            });
    } else {
        // Fallback: redirecionar
        window.location.href = '/visualizar_plano';
    }
};

// Helper: marcar campo como inválido e mostrar mensagem inline
function markInvalid(field, message) {
    try {
        field.classList.add('is-invalid');
        // procurar ou criar .invalid-feedback
        let fb = field.parentElement.querySelector('.invalid-feedback');
        if (!fb) {
            fb = document.createElement('div');
            fb.className = 'invalid-feedback';
            fb.style.display = 'block';
            field.parentElement.appendChild(fb);
        }
        fb.textContent = message;
        fb.style.display = 'block';
    } catch (e) {
        console.warn('markInvalid error', e);
    }
}

function clearInvalid(field) {
    try {
        field.classList.remove('is-invalid');
        const fb = field.parentElement.querySelector('.invalid-feedback');
        if (fb) {
            fb.textContent = '';
            fb.style.display = 'none';
        }
    } catch (e) {
        console.warn('clearInvalid error', e);
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const steps = document.querySelectorAll('.form-step');
    let currentStep = 0;

    function showStep(index) {
        steps.forEach((step, i) => {
            step.classList.toggle('active', i === index);
        });
        currentStep = index;
    }

    // Adicionar event listener ao botão Próximo
    const btnProximo = document.getElementById('btnProximo');
    if (btnProximo) {
        btnProximo.addEventListener('click', function () {
            if (typeof window.validarEProximo === 'function') {
                window.validarEProximo();
            }
        });
    }

    window.nextStep = function () {
        // Validação completa dos campos obrigatórios
        const activeStep = steps[currentStep];
        const requiredFields = activeStep.querySelectorAll('[required]');

        for (let field of requiredFields) {
            const value = field.value.trim();

            // Validação do nome - mínimo 3 caracteres
            if (field.id === 'nome') {
                if (!value) {
                    markInvalid(field, 'Por favor, preencha seu nome completo.');
                    if (window.showWarning) window.showWarning('Por favor, preencha seu nome completo.');
                    field.focus();
                    return;
                } else if (value.length < 3) {
                    markInvalid(field, 'O nome deve ter no mínimo 3 caracteres.');
                    if (window.showWarning) window.showWarning('O nome deve ter no mínimo 3 caracteres.');
                    field.focus();
                    return;
                } else {
                    clearInvalid(field);
                }
            }

            // Validação do email
            else if (field.id === 'email') {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!value) {
                    markInvalid(field, 'Por favor, preencha seu e-mail.');
                    if (window.showWarning) window.showWarning('Por favor, preencha seu e-mail.');
                    field.focus();
                    return;
                } else if (!emailRegex.test(value)) {
                    markInvalid(field, 'E-mail inválido.');
                    if (window.showWarning) window.showWarning('E-mail inválido. Verifique o formato.');
                    field.focus();
                    return;
                } else {
                    clearInvalid(field);
                }
            }

            // Validação do telefone
            else if (field.id === 'telefone') {
                const telefoneDigits = value.replace(/\D/g, '');
                if (!value) {
                    markInvalid(field, 'Por favor, preencha seu telefone.');
                    if (window.showWarning) window.showWarning('Por favor, preencha seu telefone.');
                    field.focus();
                    return;
                } else if (telefoneDigits.length !== 10 && telefoneDigits.length !== 11) {
                    markInvalid(field, 'Telefone deve conter 10 ou 11 dígitos (DDD + número).');
                    if (window.showWarning) window.showWarning('Telefone inválido. Informe DDD + número (10 ou 11 dígitos).');
                    field.focus();
                    return;
                } else {
                    clearInvalid(field);
                }
            }

            // Validação do cargo (select)
            else if (field.id === 'cargo') {
                if (!value || value === '') {
                    markInvalid(field, 'Por favor, selecione seu cargo.');
                    if (window.showWarning) window.showWarning('Por favor, selecione seu cargo.');
                    field.focus();
                    return;
                } else {
                    clearInvalid(field);
                }
            }

            // Validação genérica para outros campos
            else if (!value) {
                field.classList.add('is-invalid');
                field.focus();
                return;
            } else {
                field.classList.remove('is-invalid');
            }
        }

        if (currentStep < steps.length - 1) {
            showStep(currentStep + 1);
        }
    };

    window.prevStep = function () {
        if (currentStep > 0) {
            showStep(currentStep - 1);
        }
    };

    // Inicializa mostrando o primeiro passo
    showStep(0);

    // Máscara de telefone
    const telefoneEl = document.getElementById('telefone');
    if (telefoneEl) {
        telefoneEl.addEventListener('input', function (e) {
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
    }

    // Validação em tempo real do nome
    const nomeEl = document.getElementById('nome');
    if (nomeEl) {
        nomeEl.addEventListener('input', function (e) {
            const value = e.target.value.trim();
            if (value.length > 0 && value.length < 3) {
                markInvalid(nomeEl, 'O nome deve ter no mínimo 3 caracteres.');
            } else {
                clearInvalid(nomeEl);
            }
        });
    }

    // Validação em tempo real do email
    const emailEl = document.getElementById('email');
    if (emailEl) {
        emailEl.addEventListener('blur', function (e) {
            const value = e.target.value.trim();
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (value.length > 0 && !emailRegex.test(value)) {
                markInvalid(emailEl, 'E-mail inválido.');
            } else {
                clearInvalid(emailEl);
            }
        });
    }

    // Validação em tempo real do telefone
    if (telefoneEl) {
        telefoneEl.addEventListener('blur', function (e) {
            const telefoneDigits = e.target.value.replace(/\D/g, '');
            if (telefoneDigits.length > 0 && telefoneDigits.length !== 10 && telefoneDigits.length !== 11) {
                markInvalid(telefoneEl, 'Telefone deve conter 10 ou 11 dígitos.');
            } else {
                clearInvalid(telefoneEl);
            }
        });
    }
});
