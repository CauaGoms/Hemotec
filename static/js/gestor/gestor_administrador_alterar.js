// Alterar Administrador - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formAlterarAdmin');
    
    // Password toggle functionality
    const passwordToggles = document.querySelectorAll('.password-toggle');
    
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const input = this.previousElementSibling;
            const icon = this.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });
    
    // Password change toggle
    const changePasswordCheckbox = document.getElementById('changePassword');
    const passwordFields = document.getElementById('passwordFields');
    
    if (changePasswordCheckbox && passwordFields) {
        changePasswordCheckbox.addEventListener('change', function() {
            if (this.checked) {
                passwordFields.classList.add('active');
                passwordFields.querySelectorAll('input').forEach(input => {
                    input.setAttribute('required', 'required');
                });
            } else {
                passwordFields.classList.remove('active');
                passwordFields.querySelectorAll('input').forEach(input => {
                    input.removeAttribute('required');
                    input.value = '';
                    input.classList.remove('is-invalid', 'is-valid');
                });
            }
        });
    }
    
    // Form validation (same as adicionar)
    if (form) {
        const inputs = form.querySelectorAll('input, select');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    validateField(this);
                }
            });
        });
        
        // CPF formatting
        const cpfInput = document.getElementById('cpf');
        if (cpfInput) {
            cpfInput.addEventListener('input', function() {
                let value = this.value.replace(/\D/g, '');
                
                if (value.length <= 11) {
                    value = value.replace(/(\d{3})(\d)/, '$1.$2');
                    value = value.replace(/(\d{3})(\d)/, '$1.$2');
                    value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
                    this.value = value;
                }
            });
        }
        
        // Phone formatting
        const telefoneInput = document.getElementById('telefone');
        if (telefoneInput) {
            telefoneInput.addEventListener('input', function() {
                let value = this.value.replace(/\D/g, '');
                
                if (value.length <= 11) {
                    if (value.length <= 10) {
                        value = value.replace(/(\d{2})(\d)/, '($1) $2');
                        value = value.replace(/(\d{4})(\d)/, '$1-$2');
                    } else {
                        value = value.replace(/(\d{2})(\d)/, '($1) $2');
                        value = value.replace(/(\d{5})(\d)/, '$1-$2');
                    }
                    this.value = value;
                }
            });
        }
        
        // CEP formatting and lookup
        const cepInput = document.getElementById('cep');
        if (cepInput) {
            cepInput.addEventListener('input', function() {
                let value = this.value.replace(/\D/g, '');
                
                if (value.length <= 8) {
                    value = value.replace(/(\d{5})(\d)/, '$1-$2');
                    this.value = value;
                }
                
                if (value.replace('-', '').length === 8) {
                    lookupCEP(value.replace('-', ''));
                }
            });
        }
        
        // Form submission
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Validate all fields
            let isValid = true;
            inputs.forEach(input => {
                // Skip password fields if not changing password
                if (changePasswordCheckbox && !changePasswordCheckbox.checked && 
                    passwordFields.contains(input)) {
                    return;
                }
                
                if (!validateField(input)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                showAlert('Por favor, corrija os erros no formulário.', 'danger');
                return;
            }
            
            // Show loading state
            const submitBtn = form.querySelector('.btn-submit');
            submitBtn.disabled = true;
            submitBtn.classList.add('loading');
            
            // Prepare form data
            const formData = new FormData(form);
            const data = {};
            
            formData.forEach((value, key) => {
                if (key === 'permissao_envio_campanha' || key === 'permissao_envio_notificacao') {
                    data[key] = form.querySelector(`input[name="${key}"]`).checked;
                } else {
                    data[key] = value;
                }
            });
            
            // Add change_password flag
            if (changePasswordCheckbox) {
                data.change_password = changePasswordCheckbox.checked;
            }
            
            // Get admin ID from URL
            const adminId = window.location.pathname.split('/').pop();
            
            try {
                const response = await fetch(`/api/gestor/administrador/alterar/${adminId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    showAlert('Administrador atualizado com sucesso!', 'success');
                    setTimeout(() => {
                        window.location.href = '/gestor/administrador';
                    }, 1500);
                } else {
                    showAlert(result.detail || 'Erro ao atualizar administrador.', 'danger');
                    submitBtn.disabled = false;
                    submitBtn.classList.remove('loading');
                }
            } catch (error) {
                console.error('Erro:', error);
                showAlert('Erro ao processar requisição.', 'danger');
                submitBtn.disabled = false;
                submitBtn.classList.remove('loading');
            }
        });
    }
    
    // Field validation function
    function validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let message = '';
        
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            message = 'Este campo é obrigatório.';
        }
        
        if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                message = 'E-mail inválido.';
            }
        }
        
        if (field.id === 'cpf' && value) {
            const cpfClean = value.replace(/\D/g, '');
            if (cpfClean.length !== 11) {
                isValid = false;
                message = 'CPF deve ter 11 dígitos.';
            }
        }
        
        if (field.id === 'telefone' && value) {
            const phoneClean = value.replace(/\D/g, '');
            if (phoneClean.length < 10) {
                isValid = false;
                message = 'Telefone inválido.';
            }
        }
        
        if ((field.id === 'senha' || field.id === 'nova_senha') && value) {
            if (value.length < 6) {
                isValid = false;
                message = 'A senha deve ter no mínimo 6 caracteres.';
            }
        }
        
        if (isValid) {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
            const feedback = field.parentElement.querySelector('.invalid-feedback');
            if (feedback) feedback.remove();
        } else {
            field.classList.remove('is-valid');
            field.classList.add('is-invalid');
            
            let feedback = field.parentElement.querySelector('.invalid-feedback');
            if (!feedback) {
                feedback = document.createElement('div');
                feedback.className = 'invalid-feedback';
                field.parentElement.appendChild(feedback);
            }
            feedback.textContent = message;
        }
        
        return isValid;
    }
    
    // CEP lookup function
    async function lookupCEP(cep) {
        try {
            const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
            const data = await response.json();
            
            if (!data.erro) {
                document.getElementById('logradouro').value = data.logradouro || '';
                document.getElementById('bairro').value = data.bairro || '';
                
                // Set city if available
                if (data.localidade && data.uf) {
                    // Buscar a cidade no backend
                    buscarCidade(data.localidade, data.uf);
                }
            }
        } catch (error) {
            console.error('Erro ao buscar CEP:', error);
        }
    }
    
    async function buscarCidade(nomeCidade, uf) {
        try {
            // Buscar cidade na lista de cidades disponíveis via fetch
            const response = await fetch('/api/cidades');
            const cidades = await response.json();
            
            const cidadeEncontrada = cidades.find(cidade => 
                cidade.nome_cidade.toLowerCase() === nomeCidade.toLowerCase() && 
                cidade.sigla_estado === uf
            );
            
            if (cidadeEncontrada) {
                document.getElementById('cidade_nome').value = `${cidadeEncontrada.nome_cidade} - ${cidadeEncontrada.sigla_estado}`;
                document.getElementById('cod_cidade').value = cidadeEncontrada.cod_cidade;
            }
        } catch (error) {
            console.error('Erro ao buscar cidade:', error);
        }
    }
    
    // Show alert function
    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            <span>${message}</span>
        `;
        
        const container = document.querySelector('.form-container');
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
});
