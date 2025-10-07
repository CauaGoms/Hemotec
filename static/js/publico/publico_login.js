// Login form validation
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const emailField = document.getElementById('email');
    const passwordField = document.getElementById('password');

    // Função para mostrar mensagens de erro
    function showError(message) {
        const existingError = document.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message alert alert-danger mt-3';
        errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle me-2"></i>${message}`;
        
        form.appendChild(errorDiv);
        
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.remove();
            }
        }, 5000);
    }

    // Função para mostrar mensagens de aviso
    function showWarning(message) {
        const existingWarning = document.querySelector('.warning-message');
        if (existingWarning) {
            existingWarning.remove();
        }
        
        const warningDiv = document.createElement('div');
        warningDiv.className = 'warning-message alert alert-warning mt-3';
        warningDiv.innerHTML = `<i class="fas fa-exclamation-triangle me-2"></i>${message}`;
        
        form.appendChild(warningDiv);
        
        setTimeout(() => {
            if (warningDiv.parentNode) {
                warningDiv.remove();
            }
        }, 5000);
    }

    // Disponibilizar funções globalmente
    window.showError = showError;
    window.showWarning = showWarning;

    // Função para marcar campo como inválido
    function markInvalid(field, message) {
        field.classList.add('is-invalid');
        let feedback = field.parentElement.querySelector('.invalid-feedback');
        if (!feedback) {
            feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            field.parentElement.appendChild(feedback);
        }
        feedback.textContent = message;
    }

    // Função para limpar validação do campo
    function clearInvalid(field) {
        field.classList.remove('is-invalid');
        const feedback = field.parentElement.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.remove();
        }
    }

    // Validação de email em tempo real
    emailField.addEventListener('blur', function() {
        const email = this.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (!email) {
            markInvalid(this, 'E-mail é obrigatório');
        } else if (!emailRegex.test(email)) {
            markInvalid(this, 'E-mail inválido');
        } else {
            clearInvalid(this);
        }
    });

    // Validação de senha em tempo real
    passwordField.addEventListener('blur', function() {
        const password = this.value;
        
        if (!password) {
            markInvalid(this, 'Senha é obrigatória');
        } else {
            clearInvalid(this);
        }
    });

    // Limpar erros quando o usuário começar a digitar
    emailField.addEventListener('input', function() {
        if (this.classList.contains('is-invalid')) {
            clearInvalid(this);
        }
    });

    passwordField.addEventListener('input', function() {
        if (this.classList.contains('is-invalid')) {
            clearInvalid(this);
        }
    });

    // Validação no envio do formulário
    form.addEventListener('submit', function(e) {
        let hasErrors = false;
        
        // Validar email
        const email = emailField.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (!email) {
            markInvalid(emailField, 'E-mail é obrigatório');
            hasErrors = true;
        } else if (!emailRegex.test(email)) {
            markInvalid(emailField, 'E-mail inválido');
            hasErrors = true;
        } else {
            clearInvalid(emailField);
        }

        // Validar senha
        const password = passwordField.value;
        
        if (!password) {
            markInvalid(passwordField, 'Senha é obrigatória');
            hasErrors = true;
        } else {
            clearInvalid(passwordField);
        }

        // Impedir envio se houver erros
        if (hasErrors) {
            e.preventDefault();
            showWarning('Por favor, corrija os erros no formulário.');
            // Focar no primeiro campo com erro
            const firstInvalidField = form.querySelector('.is-invalid');
            if (firstInvalidField) {
                firstInvalidField.focus();
            }
        }
    });
});