document.addEventListener('DOMContentLoaded', function () {
    const newAppointmentEl = document.getElementById('new-appointment');
    const confirmBtn = document.getElementById('confirmBtn');

    let novaDataSelecionada = null;
    let novaHoraSelecionada = null;
    let novoLocalSelecionado = null;

    // Inicializa página
    function inicializarPagina() {
        // Garante que o calendário inicia no mês atual
        if (typeof currentDate === 'undefined' || !currentDate || !(currentDate instanceof Date)) {
            const today = new Date();
            window.currentDate = new Date(today.getFullYear(), today.getMonth(), 1);
        } else {
            const today = new Date();
            currentDate.setFullYear(today.getFullYear());
            currentDate.setMonth(today.getMonth());
            currentDate.setDate(1);
        }

        // Seleciona o primeiro hemocentro (ou o atual, se houver)
        const firstLocationCard = document.querySelector('.location-card.active') || document.querySelector('.location-card');
        if (firstLocationCard) {
            const locationId = firstLocationCard.getAttribute('data-unidade-id');
            selectLocation(locationId, firstLocationCard);
            novoLocalSelecionado = locationId;
        }
    }

    // Sobrescrever função de seleção de local
    const originalSelectLocation = window.selectLocation;
    window.selectLocation = function (locationId, element) {
        novoLocalSelecionado = locationId;
        originalSelectLocation(locationId, element);
    };

    // Sobrescrever função de seleção de data
    const originalSelectDay = window.selectDay;
    window.selectDay = function (day, element) {
        originalSelectDay(day, element);
        novaDataSelecionada = selectedDate;
        atualizarResumo();
    };

    // Sobrescrever função de seleção de horário
    const originalSelectTime = window.selectTime;
    window.selectTime = function (time, element) {
        originalSelectTime(time, element);
        novaHoraSelecionada = selectedTime;
        atualizarResumo();
    };

    // Atualizar resumo do novo agendamento
    function atualizarResumo() {
        if (novaDataSelecionada && novaHoraSelecionada) {
            const diasSemana = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'];
            const meses = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'];

            const data = new Date(novaDataSelecionada);
            const diaSemana = diasSemana[data.getDay()];
            const dia = data.getDate();
            const mes = meses[data.getMonth()];
            const ano = data.getFullYear();

            newAppointmentEl.textContent = `${diaSemana}, ${dia} de ${mes} de ${ano} - ${novaHoraSelecionada}`;
            newAppointmentEl.classList.remove('text-muted');
            confirmBtn.disabled = false;
            confirmBtn.classList.remove('disabled');
        } else {
            newAppointmentEl.textContent = "Selecione uma nova data e horário";
            newAppointmentEl.classList.add('text-muted');
            confirmBtn.disabled = true;
            confirmBtn.classList.add('disabled');
        }
    }

    // Sobrescrever função confirmAppointment
    window.confirmAppointment = function () {
        if (!novaDataSelecionada || !novaHoraSelecionada || !novoLocalSelecionado) {
            alert('Por favor, selecione uma data, horário e local para o novo agendamento.');
            return;
        }

        // Formatar data e hora no formato esperado pelo backend (YYYY-MM-DD HH:MM)
        const data = new Date(novaDataSelecionada);
        const ano = data.getFullYear();
        const mes = String(data.getMonth() + 1).padStart(2, '0');
        const dia = String(data.getDate()).padStart(2, '0');
        const dataHoraFormatada = `${ano}-${mes}-${dia} ${novaHoraSelecionada}`;

        // Preencher campos ocultos do formulário
        document.getElementById('input-data-hora').value = dataHoraFormatada;
        document.getElementById('input-local-agendamento').value = novoLocalSelecionado;

        // Submeter formulário
        document.getElementById('form-alterar-agendamento').submit();
    };

    inicializarPagina();
});
