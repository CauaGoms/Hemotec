// Validação de Token - JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const tokenInput = document.getElementById('token');
    const submitBtn = document.querySelector('.btn-recovery');
    
    // Função para mostrar mensagens de erro
    function showError(message) {
        // Remove mensagem de erro anterior se existir
        const existingError = document.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        // Cria nova mensagem de erro
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message alert alert-danger mt-3';
        errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle me-2"></i>${message}`;
        
        // Insere a mensagem após o formulário
        form.appendChild(errorDiv);
        
        // Remove a mensagem após 5 segundos
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
    
    // Função para validar formato do token
    function validateTokenFormat(token) {
        // Token deve ter exatamente 6 dígitos
        const tokenRegex = /^[0-9]{6}$/;
        return tokenRegex.test(token);
    }
    
    // Formatação automática do campo token (apenas números)
    tokenInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/[^0-9]/g, '');
        if (value.length > 6) {
            value = value.substring(0, 6);
        }
        e.target.value = value;
        
        // Remove mensagens de erro quando o usuário digita
        const errorMessage = document.querySelector('.error-message');
        if (errorMessage) {
            errorMessage.remove();
        }
    });
    
    // Função para simular validação do token no servidor
    async function validateToken(token) {
        // Simula delay de requisição
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Simula diferentes cenários de resposta
        const scenarios = [
            { valid: true, message: 'Token válido' },
            { valid: false, message: 'Token inválido ou expirado' },
            { valid: false, message: 'Token não encontrado' },
            { valid: false, message: 'Token já foi utilizado' }
        ];
        
        // Para demonstração, tokens específicos retornam cenários diferentes
        if (token === '123456') {
            return scenarios[0]; // Sucesso
        } else if (token === '000000') {
            return scenarios[1]; // Token inválido
        } else if (token === '111111') {
            return scenarios[2]; // Token não encontrado
        } else if (token === '222222') {
            return scenarios[3]; // Token já utilizado
        } else {
            // Comportamento aleatório para outros tokens
            return scenarios[Math.floor(Math.random() * scenarios.length)];
        }
    }
    
    // Função para mostrar loading
    function showLoading() {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Validando...';
    }
    
    // Função para esconder loading
    function hideLoading() {
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Validar';
    }
    
    // Manipulador do envio do formulário
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const token = tokenInput.value.trim();
        
        // Validações básicas
        if (!token) {
            showError('Por favor, digite o código de verificação.');
            tokenInput.focus();
            return;
        }
        
        if (!validateTokenFormat(token)) {
            showError('O código deve conter exatamente 6 dígitos.');
            tokenInput.focus();
            return;
        }
        
        try {
            showLoading();
            
            // Simula validação no servidor
            const result = await validateToken(token);
            
            hideLoading();
            
            if (result.valid) {
                showSuccess('Código validado com sucesso! Redirecionando...');
                
                // Redireciona após 2 segundos
                setTimeout(() => {
                    window.location.href = '/criar_nova_senha';
                }, 2000);
            } else {
                showError(result.message);
                tokenInput.value = '';
                tokenInput.focus();
            }
            
        } catch (error) {
            hideLoading();
            showError('Erro de conexão. Tente novamente.');
            console.error('Erro na validação:', error);
        }
    });
    
    // Função para reenviar código
    const resendLink = document.querySelector('a[href*="redefinir-senha"]');
    if (resendLink) {
        resendLink.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Simula reenvio do código
            showSuccess('Novo código enviado para seu e-mail!');
            
            // Opcional: implementar cooldown para reenvio
            this.style.pointerEvents = 'none';
            this.style.opacity = '0.5';
            this.textContent = 'Aguarde 60s para reenviar';
            
            let countdown = 60;
            const countdownInterval = setInterval(() => {
                countdown--;
                this.textContent = `Aguarde ${countdown}s para reenviar`;
                
                if (countdown <= 0) {
                    clearInterval(countdownInterval);
                    this.style.pointerEvents = 'auto';
                    this.style.opacity = '1';
                    this.textContent = 'Não recebeu o código? Solicitar novamente';
                }
            }, 1000);
        });
    }
    
    // Auto-focus no campo de token
    tokenInput.focus();
});

