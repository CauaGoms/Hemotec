document.addEventListener('DOMContentLoaded', function() {
    // Seleciona a aba de "Próximos Agendamentos" e a mensagem de "sem agendamentos"
    const proximaAba = document.getElementById('pills-proximos');
    const mensagemSemAgendamentos = proximaAba.querySelector('.no-appointments-message');

    // Verifica se existe algum card de agendamento na aba
    const agendamentosFuturos = proximaAba.querySelectorAll('.appointment-card');

    // Se não houver nenhum card, esconde os exemplos e mostra a mensagem
    if (agendamentosFuturos.length === 0) {
        // Se você tiver cards de exemplo no HTML, pode escondê-los aqui
        // agendamentosFuturos.forEach(card => card.style.display = 'none');
        
        if (mensagemSemAgendamentos) {
            mensagemSemAgendamentos.style.display = 'block';
        }
    } else {
         if (mensagemSemAgendamentos) {
            mensagemSemAgendamentos.style.display = 'none';
        }
    }

    // Adicionar funcionalidade para botões de ação
    const btnRagendar = document.querySelectorAll('.btn-outline-primary');
    const btnCancelar = document.querySelectorAll('.btn-outline-danger');
    
    btnRagendar.forEach(btn => {
        btn.addEventListener('click', function() {
            window.location.href = '/doador/agendamento';
        });
    });
    
    btnCancelar.forEach(btn => {
        btn.addEventListener('click', function() {
            if (confirm('Tem certeza que deseja cancelar este agendamento?')) {
                // Aqui você pode adicionar a lógica para cancelar o agendamento
                console.log('Agendamento cancelado');
            }
        });
    });
});

// Função para navegar de volta à página de agendamento
function voltarParaAgendamento() {
    window.location.href = '/doador/agendamento';
}
