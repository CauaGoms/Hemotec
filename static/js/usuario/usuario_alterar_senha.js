// Criar Nova Senha - JavaScript
console.log('JS de criar nova senha carregado e executado');
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const novaSenhaInput = document.getElementById('nova_senha');
    const confirmarSenhaInput = document.getElementById('confirmar_senha');
    const submitBtn = document.querySelector('.btn-recovery');
    
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
    
    // Função para mostrar mensagens de sucesso
    function showSuccess(message) {
        const existingSuccess = document.querySelector('.success-message');
        if (existingSuccess) {
            existingSuccess.remove();
        }
        
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message alert alert-success mt-3';
        successDiv.innerHTML = `<i class="fas fa-check-circle me-2"></i>${message}`;
        
        form.appendChild(successDiv);
        
        setTimeout(() => {
            if (successDiv.parentNode) {
                successDiv.remove();
            }
        }, 3000);
    }
    
    // Função para validar força da senha
    function validatePasswordStrength(password) {
        const errors = [];
        
        if (password.length < 8) {
            errors.push('A senha deve ter pelo menos 8 caracteres');
        }
        
        if (!/[A-Z]/.test(password)) {
            errors.push('A senha deve conter pelo menos uma letra maiúscula');
        }
        
        if (!/[a-z]/.test(password)) {
            errors.push('A senha deve conter pelo menos uma letra minúscula');
        }
        
        if (!/[0-9]/.test(password)) {
            errors.push('A senha deve conter pelo menos um número');
        }
        
        if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) {
            errors.push('A senha deve conter pelo menos um caractere especial');
        }
        
        return {
            isValid: errors.length === 0,
            errors: errors
        };
    }
    
    // Função para calcular força da senha
    function calculatePasswordStrength(password) {
        let strength = 0;
        
        if (password.length >= 8) strength += 20;
        if (password.length >= 12) strength += 10;
        if (/[A-Z]/.test(password)) strength += 20;
        if (/[a-z]/.test(password)) strength += 20;
        if (/[0-9]/.test(password)) strength += 15;
        if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) strength += 15;
        
        return Math.min(strength, 100);
    }
    
    // Função para mostrar indicador de força da senha
    function showPasswordStrength(password) {
        // Remove indicador anterior
        const existingIndicator = document.querySelector('.password-strength');
        if (existingIndicator) {
            existingIndicator.remove();
        }
        
        if (!password) return;
        
        const strength = calculatePasswordStrength(password);
        const strengthDiv = document.createElement('div');
        strengthDiv.className = 'password-strength mt-2';
        
        let strengthText = '';
        let strengthClass = '';
        
        if (strength < 40) {
            strengthText = 'Fraca';
            strengthClass = 'text-danger';
        } else if (strength < 70) {
            strengthText = 'Média';
            strengthClass = 'text-warning';
        } else {
            strengthText = 'Forte';
            strengthClass = 'text-success';
        }
        
        strengthDiv.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <small>Força da senha:</small>
                <small class="${strengthClass} fw-bold">${strengthText}</small>
            </div>
            <div class="progress mt-1" style="height: 4px;">
                <div class="progress-bar ${strengthClass.replace('text-', 'bg-')}" 
                     style="width: ${strength}%"></div>
            </div>
        `;
        
        novaSenhaInput.parentNode.appendChild(strengthDiv);
    }

    
    // Event listener para mostrar força da senha
    novaSenhaInput.addEventListener('input', function() {
        showPasswordStrength(this.value);
        
        // Remove mensagens de erro quando o usuário digita
        const errorMessage = document.querySelector('.error-message');
        if (errorMessage) {
            errorMessage.remove();
        }
    });
    
    // Event listener para confirmação de senha
    confirmarSenhaInput.addEventListener('input', function() {
        const errorMessage = document.querySelector('.error-message');
        if (errorMessage) {
            errorMessage.remove();
        }
    });
    
    // Função para simular alteração de senha no servidor
    async function changePassword(novaSenha) {
        // Simula delay de requisição
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // Simula diferentes cenários de resposta
        const scenarios = [
            { success: true, message: 'Senha alterada com sucesso' },
            { success: false, message: 'Erro interno do servidor' },
            { success: false, message: 'Sessão expirada. Tente novamente.' },
            { success: false, message: 'A nova senha não pode ser igual à senha anterior' }
        ];
        
        // Para demonstração, senhas específicas retornam cenários diferentes
        if (novaSenha === 'MinhaNovaSenh@123') {
            return scenarios[0]; // Sucesso
        } else if (novaSenha === 'ErroServidor123!') {
            return scenarios[1]; // Erro servidor
        } else if (novaSenha === 'SessaoExpirada123!') {
            return scenarios[2]; // Sessão expirada
        } else if (novaSenha === 'SenhaAntiga123!') {
            return scenarios[3]; // Senha igual à anterior
        } else {
            // Sucesso para outras senhas válidas
            return scenarios[0];
        }
    }
    
    // Função para mostrar loading
    function showLoading() {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Alterando Senha...';
    }
    
    // Função para esconder loading
    function hideLoading() {
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Alterar Senha';
    }
    
    // Manipulador do envio do formulário
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const novaSenha = novaSenhaInput.value.trim();
        const confirmarSenha = confirmarSenhaInput.value.trim();
        
        // Validações básicas
        if (!novaSenha) {
            showError('Por favor, digite sua nova senha.');
            novaSenhaInput.focus();
            return;
        }
        
        if (!confirmarSenha) {
            showError('Por favor, confirme sua nova senha.');
            confirmarSenhaInput.focus();
            return;
        }
        
        // Validação de força da senha
        const strengthValidation = validatePasswordStrength(novaSenha);
        const strength = calculatePasswordStrength(novaSenha);
        if (!strengthValidation.isValid) {
            showError(strengthValidation.errors.join('<br>'));
            novaSenhaInput.focus();
            return;
        }
        if (strength < 40) {
            showError('A senha está muito fraca. Crie uma senha mais forte!');
            novaSenhaInput.focus();
            return;
        }
        
        // Validação de confirmação
        if (novaSenha !== confirmarSenha) {
            showError('As senhas não coincidem. Verifique e tente novamente.');
            confirmarSenhaInput.focus();
            return;
        }
        
        try {
            showLoading();
            
            // Simula alteração no servidor
            const result = await changePassword(novaSenha);
            
            hideLoading();
            
            if (result.success) {
                showSuccess('Senha alterada com sucesso! Redirecionando...');
                
                // Redireciona após 2 segundos
                setTimeout(() => {
                    window.location.href = '/dados_cadastrais';
                }, 2000);
            } else {
                showError(result.message);
                
                // Se for erro de sessão, redireciona para o início
                if (result.message.includes('Sessão expirada')) {
                    setTimeout(() => {
                        window.location.href = '/dados_cadastrais';
                    }, 3000);
                }
            }
            
        } catch (error) {
            hideLoading();
            showError('Erro de conexão. Tente novamente.');
            console.error('Erro na alteração:', error);
        }
    });
    
    // Auto-focus no primeiro campo
    novaSenhaInput.focus();
});

