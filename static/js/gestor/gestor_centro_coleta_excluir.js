// Excluir Centro de Coleta - JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const deleteForm = document.getElementById('formExcluirCentro');
    
    if (deleteForm) {
        deleteForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const unidadeId = window.location.pathname.split('/').pop();
            
            try {
                const response = await fetch(`/api/gestor/centro-coleta/excluir/${unidadeId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    alert('Centro de coleta excluído com sucesso!');
                    window.location.href = '/gestor/centro-coleta';
                } else {
                    alert('Erro: ' + result.message);
                }
            } catch (error) {
                console.error('Erro:', error);
                alert('Erro ao excluir centro de coleta');
            }
        });
    }
});
