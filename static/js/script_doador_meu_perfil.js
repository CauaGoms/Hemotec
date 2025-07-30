function editProfile() {
            alert('Abrindo edição de perfil...');
            // Implementar lógica para edição do perfil
        }
        
        function editHealthInfo() {
            alert('Abrindo edição de informações de saúde...');
            // Implementar lógica para edição das informações de saúde
        }
        
        function editProfessionalInfo() {
            alert('Abrindo edição de informações profissionais...');
            // Implementar lógica para edição das informações profissionais
        }
        
        function changePassword() {
            alert('Abrindo formulário para alteração de senha...');
            // Implementar lógica para alteração de senha
        }
        
        function confirmAccountDeletion() {
            if (confirm('Tem certeza que deseja encerrar sua conta? Esta ação é irreversível e todos os seus dados serão permanentemente removidos.')) {
                alert('Sua conta será encerrada. Você será redirecionado para a página inicial.');
                // Implementar lógica para encerramento de conta
                // window.location.href = 'login.html';
            }
        }
        
        // Ativar tooltips
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });