// JavaScript específico para a página de agendamentos
document.addEventListener('DOMContentLoaded', function() {
    let agendamentoParaCancelar = null;

    // Função para cancelar agendamento
    const botoesCancel = document.querySelectorAll('.btn-cancelar');
    botoesCancel.forEach(botao => {
        botao.addEventListener('click', function() {
            agendamentoParaCancelar = this.getAttribute('data-id');
            const modal = new bootstrap.Modal(document.getElementById('cancelModal'));
            modal.show();
        });
    });

    // Confirmar cancelamento
    document.getElementById('confirmCancel').addEventListener('click', function() {
        if (agendamentoParaCancelar) {
            // Aqui você pode adicionar a lógica para cancelar o agendamento
            console.log('Cancelando agendamento:', agendamentoParaCancelar);
            
            // Simular remoção do card
            const card = document.querySelector(`[data-id="${agendamentoParaCancelar}"]`).closest('.appointment-card');
            card.style.transition = 'opacity 0.3s ease';
            card.style.opacity = '0';
            
            setTimeout(() => {
                card.remove();
                verificarAgendamentosVazios();
            }, 300);

            // Fechar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('cancelModal'));
            modal.hide();
            
            agendamentoParaCancelar = null;
        }
    });

    // Função para reagendar
    const botoesReagendar = document.querySelectorAll('.btn-reagendar');
    botoesReagendar.forEach(botao => {
        botao.addEventListener('click', function() {
            const agendamentoId = this.getAttribute('data-id');
            // Redirecionar para página de reagendamento
            window.location.href = `/doador/reagendamento?id=${agendamentoId}`;
        });
    });

    // Verificar se há agendamentos para mostrar mensagem vazia
    function verificarAgendamentosVazios() {
        const agendamentos = document.querySelectorAll('.appointment-card');
        const mensagemVazia = document.querySelector('.no-appointments-message');
        
        if (agendamentos.length === 0) {
            mensagemVazia.style.display = 'block';
        } else {
            mensagemVazia.style.display = 'none';
        }
    }

    // Verificar inicialmente
    verificarAgendamentosVazios();
});
