// Excluir Administrador - JavaScript
// Updated: 2025-11-25

document.addEventListener('DOMContentLoaded', function() {
    const deleteForm = document.getElementById('formExcluirAdmin');
    
    if (deleteForm) {
        deleteForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Show loading state
            const submitBtn = deleteForm.querySelector('.btn-confirm-delete');
            const cancelBtn = deleteForm.querySelector('.btn-cancel');
            submitBtn.disabled = true;
            cancelBtn.style.pointerEvents = 'none';
            submitBtn.classList.add('loading');
            
            // Get admin ID from URL
            const adminId = window.location.pathname.split('/').pop();
            
            try {
                const response = await fetch(`/api/gestor/administrador/excluir/${adminId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    // Show success message
                    showAlert('Administrador excluído com sucesso!', 'success');
                    
                    // Redirect after delay
                    setTimeout(() => {
                        window.location.href = '/gestor/administrador';
                    }, 1500);
                } else {
                    showAlert(result.detail || 'Erro ao excluir administrador.', 'danger');
                    submitBtn.disabled = false;
                    cancelBtn.style.pointerEvents = 'auto';
                    submitBtn.classList.remove('loading');
                }
            } catch (error) {
                console.error('Erro:', error);
                showAlert('Erro ao processar requisição.', 'danger');
                submitBtn.disabled = false;
                cancelBtn.style.pointerEvents = 'auto';
                submitBtn.classList.remove('loading');
            }
        });
    }
    
    // Show alert function
    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            <span>${message}</span>
        `;
        
        const container = document.querySelector('.delete-container');
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
    
    // Animate elements on load
    const warningAlert = document.querySelector('.warning-alert');
    const adminCard = document.querySelector('.admin-info-card');
    const confirmSection = document.querySelector('.confirmation-section');
    
    setTimeout(() => {
        if (warningAlert) warningAlert.style.animation = 'fadeIn 0.5s ease';
    }, 100);
    
    setTimeout(() => {
        if (adminCard) adminCard.style.animation = 'fadeIn 0.5s ease';
    }, 300);
    
    setTimeout(() => {
        if (confirmSection) confirmSection.style.animation = 'fadeIn 0.5s ease';
    }, 500);
});
