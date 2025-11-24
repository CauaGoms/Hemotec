// Máscaras para campos
function applyCPFMask(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length <= 11) {
        value = value.replace(/(\d{3})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    }
    input.value = value;
}

function applyPhoneMask(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length <= 11) {
        value = value.replace(/^(\d{2})(\d)/g, '($1) $2');
        value = value.replace(/(\d)(\d{4})$/, '$1-$2');
    }
    input.value = value;
}

function applyCEPMask(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length <= 8) {
        value = value.replace(/^(\d{5})(\d)/, '$1-$2');
    }
    input.value = value;
}

// Validação de CPF
function validateCPF(cpf) {
    cpf = cpf.replace(/\D/g, '');
    
    if (cpf.length !== 11) return false;
    if (/^(\d)\1{10}$/.test(cpf)) return false;
    
    let sum = 0;
    for (let i = 0; i < 9; i++) {
        sum += parseInt(cpf.charAt(i)) * (10 - i);
    }
    let digit1 = 11 - (sum % 11);
    if (digit1 > 9) digit1 = 0;
    
    if (parseInt(cpf.charAt(9)) !== digit1) return false;
    
    sum = 0;
    for (let i = 0; i < 10; i++) {
        sum += parseInt(cpf.charAt(i)) * (11 - i);
    }
    let digit2 = 11 - (sum % 11);
    if (digit2 > 9) digit2 = 0;
    
    return parseInt(cpf.charAt(10)) === digit2;
}

// Toggle password visibility
function togglePassword(fieldId) {
    const field = document.getElementById(fieldId);
    const icon = document.getElementById(fieldId + '-icon');
    
    if (field.type === 'password') {
        field.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        field.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// Buscar CEP
async function buscarCEP(cep) {
    cep = cep.replace(/\D/g, '');
    
    if (cep.length !== 8) return;
    
    try {
        const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
        const data = await response.json();
        
        if (!data.erro) {
            document.getElementById('rua_usuario').value = data.logradouro || '';
            document.getElementById('bairro_usuario').value = data.bairro || '';
            
            // Tentar encontrar a cidade no select
            const cidadeSelect = document.getElementById('cidade_usuario');
            const options = cidadeSelect.options;
            for (let i = 0; i < options.length; i++) {
                if (options[i].text.includes(data.localidade)) {
                    cidadeSelect.selectedIndex = i;
                    break;
                }
            }
        }
    } catch (error) {
        console.error('Erro ao buscar CEP:', error);
    }
}

// Mostrar toast
function showToast(message, type = 'info') {
    const existingToasts = document.querySelectorAll('.toast-notification');
    existingToasts.forEach(toast => toast.remove());

    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'times-circle' : 'info-circle'} me-2"></i>
            ${message}
        </div>
    `;

    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#0066cc'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        z-index: 9999;
        animation: slideIn 0.3s ease;
    `;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Adicionar animações CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    // Aplicar máscaras
    const cpfInput = document.getElementById('cpf');
    const telefoneInput = document.getElementById('telefone');
    const cepInput = document.getElementById('cep_usuario');
    
    if (cpfInput) {
        cpfInput.addEventListener('input', () => applyCPFMask(cpfInput));
    }
    
    if (telefoneInput) {
        telefoneInput.addEventListener('input', () => applyPhoneMask(telefoneInput));
    }
    
    if (cepInput) {
        cepInput.addEventListener('input', () => applyCEPMask(cepInput));
        cepInput.addEventListener('blur', () => buscarCEP(cepInput.value));
    }
    
    // Validação e envio do formulário
    const form = document.getElementById('collaboratorForm');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Validar CPF
            const cpf = document.getElementById('cpf').value;
            if (!validateCPF(cpf)) {
                showToast('CPF inválido!', 'error');
                return;
            }
            
            // Validar senha
            const senha = document.getElementById('senha').value;
            if (senha.length < 6) {
                showToast('A senha deve ter no mínimo 6 caracteres!', 'error');
                return;
            }
            
            // Desabilitar botão de envio
            const submitBtn = document.getElementById('submitBtn');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Salvando...';
            
            try {
                // Coletar dados do formulário
                const formData = new FormData(form);
                
                // Enviar para o servidor
                const response = await fetch('/api/administrador/colaboradores/adicionar', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    // Mostrar modal de sucesso
                    const successModal = new bootstrap.Modal(document.getElementById('successModal'));
                    successModal.show();
                    
                    // Limpar formulário
                    form.reset();
                } else {
                    showToast(result.message || 'Erro ao cadastrar colaborador', 'error');
                }
            } catch (error) {
                console.error('Erro:', error);
                showToast('Erro ao cadastrar colaborador. Tente novamente.', 'error');
            } finally {
                // Reabilitar botão
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-save"></i> Salvar Colaborador';
            }
        });
    }
});
