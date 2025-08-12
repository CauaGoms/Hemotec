document.addEventListener('DOMContentLoaded', function() {
    // --- DADOS SIMULADOS DO AGENDAMENTO ATUAL ---
    const agendamentoAtual = {
        local: "Hemocentro Regional de Cachoeiro",
        endereco: "Rua Dr. Raulino de Oliveira, 345 - Centro",
        horarioFuncionamento: "Seg-Sex: 7h-18h | Sáb: 7h-12h",
        data: "27/06/2025",
        hora: "10:30",
        diaSemana: "Sexta-feira"
    };

    const currentAppointmentEl = document.getElementById('current-appointment');
    const newAppointmentEl = document.getElementById('new-appointment');
    const confirmBtn = document.getElementById('confirmBtn');

    // Inicializa resumo e dados do agendamento atual
    function inicializarPagina() {
        document.getElementById('location-name').textContent = agendamentoAtual.local;
        document.getElementById('location-address').textContent = agendamentoAtual.endereco;
        document.getElementById('location-hours').textContent = agendamentoAtual.horarioFuncionamento;
        currentAppointmentEl.textContent = `${agendamentoAtual.diaSemana}, ${agendamentoAtual.data.replace(/\//g, ' de ')} - ${agendamentoAtual.hora}`;

        // Seleciona o primeiro hemocentro automaticamente e abre o calendário no mês atual
        // Não sobrescreva a variável global, apenas inicialize se necessário
        if (typeof currentDate === 'undefined' || !currentDate || !(currentDate instanceof Date)) {
            const today = new Date();
            window.currentDate = new Date(today.getFullYear(), today.getMonth(), 1);
        } else {
            // Garante que está no mês atual
            const today = new Date();
            currentDate.setFullYear(today.getFullYear());
            currentDate.setMonth(today.getMonth());
            currentDate.setDate(1);
        }
        const firstLocationCard = document.querySelector('.location-card');
        if (firstLocationCard) {
            selectLocation(1, firstLocationCard);
        }
    }

    window.atualizarResumoReagendamento = function(novaData, novaHora) {
        if (novaData && novaHora) {
            newAppointmentEl.textContent = `${novaData} - ${novaHora}`;
            newAppointmentEl.classList.remove('text-muted');
            confirmBtn.disabled = false;
        } else {
            newAppointmentEl.textContent = "Selecione uma nova data e horário";
            newAppointmentEl.classList.add('text-muted');
            confirmBtn.disabled = true;
        }
    };

    window.confirmReschedule = function() {
        const novaInfo = newAppointmentEl.textContent;
        alert(`Agendamento alterado com sucesso para: ${novaInfo}`);
        window.location.href = '/doador/agendamento/historico_agendamentos';
    };

    inicializarPagina();
});
