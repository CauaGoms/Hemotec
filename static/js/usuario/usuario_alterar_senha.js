// Alterar Senha - JavaScript
console.log('JS de alterar senha carregado e executado');
document.addEventListener('DOMContentLoaded', function () {
    const novaSenhaInput = document.getElementById('nova_senha');
    const confirmarSenhaInput = document.getElementById('confirmar_senha');

    // Função para calcular força da senha
    function calculatePasswordStrength(password) {
        let strength = 0;

        if (password.length >= 6) strength += 20;
        if (password.length >= 8) strength += 10;
        if (password.length >= 12) strength += 10;
        if (/[A-Z]/.test(password)) strength += 20;
        if (/[a-z]/.test(password)) strength += 20;
        if (/[0-9]/.test(password)) strength += 10;
        if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) strength += 10;

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
    if (novaSenhaInput) {
        novaSenhaInput.addEventListener('input', function () {
            showPasswordStrength(this.value);
        });

        // Auto-focus no primeiro campo
        novaSenhaInput.focus();
    }
});

