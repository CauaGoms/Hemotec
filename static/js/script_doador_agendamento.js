// Dados de exemplo para os hemocentros
const locations = {
    1: {
        name: "Hemocentro Regional de Cachoeiro",
        address: "Rua Dr. Raulino de Oliveira, 345 - Centro",
        distance: "1.2 km de distância",
        hours: "Seg-Sex: 7h-18h | Sáb: 7h-12h",
        features: ["Estacionamento", "Acessível"],
        image: "https://images.unsplash.com/photo-1584036561566-baf8f5f1b144?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1632&q=80"
    },
    2: {
        name: "Hospital Santa Casa",
        address: "Av. Beira Rio, 1200 - Independência",
        distance: "2.5 km de distância",
        hours: "Seg-Sex: 8h-17h",
        features: ["Estacionamento"],
        image: "https://images.unsplash.com/photo-1579684385127-1ef15d508118?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80"
    },
    3: {
        name: "Unidade Móvel - Praça Jerônimo Monteiro",
        address: "Praça Jerônimo Monteiro - Centro",
        distance: "3.1 km de distância",
        hours: "Ter e Qui: 9h-15h",
        features: ["Unidade Móvel"],
        image: "https://images.unsplash.com/photo-1581093450021-4a7360e9a9d4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80"
    }
};

// Variáveis globais
let selectedLocation = null;
let selectedDate = null;
let selectedTime = null;
let currentDate = new Date(2025, 5, 1); // Junho de 2025

// Selecionar um hemocentro
function selectLocation(locationId, element) {
    selectedLocation = locationId;

    // Atualizar a lista de hemocentros
    document.querySelectorAll('.location-card').forEach(card => {
        card.style.borderLeft = '4px solid #ddd';
    });
    element.style.borderLeft = '4px solid var(--hemotec-red)';

    // Mostrar detalhes do hemocentro selecionado
    document.getElementById('locationDetails').style.display = 'none';
    document.getElementById('selectedLocation').style.display = 'block';

    // Atualizar o calendário
    updateCalendar();

    // Resetar seleções de data e horário
    selectedDate = null;
    selectedTime = null;
    document.getElementById('confirmBtn').disabled = true;
    document.getElementById('timeSlots').innerHTML = '<p class="text-muted">Selecione uma data para ver os horários disponíveis</p>';

    // Scroll para a seção de agendamento
    document.getElementById('selectedLocation').scrollIntoView({ behavior: 'smooth' });
}

// Atualizar o calendário
function updateCalendar() {
    const monthNames = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
    document.getElementById('currentMonth').textContent = `${monthNames[currentDate.getMonth()]} ${currentDate.getFullYear()}`;

    const firstDay = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
    const lastDay = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDay = firstDay.getDay();

    let calendarHTML = '';
    let dayCount = 1;

    // Dias vazios no início do mês
    for (let i = 0; i < startingDay; i++) {
        calendarHTML += '<div class="col p-1"></div>';
    }

    // Dias do mês
    for (let i = startingDay; i < 42; i++) {
        if (dayCount <= daysInMonth) {
            const dayDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), dayCount);
            const dayName = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"][dayDate.getDay()];

            // Verificar se o dia está disponível (exemplo: fins de semana para algumas unidades)
            let isAvailable = true;
            if (selectedLocation === 3) { // Unidade móvel só funciona Ter e Qui
                isAvailable = dayDate.getDay() === 2 || dayDate.getDay() === 4;
            } else if (dayDate.getDay() === 0) { // Domingo fechado
                isAvailable = false;
            }

            // Verificar se é uma data passada
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            const isPast = dayDate < today;

            calendarHTML += `
                        <div class="col p-1">
                            <div class="calendar-day ${isPast ? 'unavailable' : ''} ${!isAvailable ? 'unavailable' : ''} ${selectedDate && selectedDate.getDate() === dayCount && selectedDate.getMonth() === currentDate.getMonth() ? 'selected' : ''}" 
                                 onclick="${isPast || !isAvailable ? '' : `selectDay(${dayCount}, this)`}">
                                <div class="day-number">${dayCount}</div>
                                <div class="day-name">${dayName}</div>
                            </div>
                        </div>
                    `;
            dayCount++;
        } else {
            calendarHTML += '<div class="col p-1"></div>';
        }
    }

    document.getElementById('calendarDays').innerHTML = calendarHTML;
}

// Mudar mês
function changeMonth(direction) {
    currentDate.setMonth(currentDate.getMonth() + direction);
    updateCalendar();

    // Resetar seleções de data e horário
    selectedDate = null;
    selectedTime = null;
    document.getElementById('confirmBtn').disabled = true;
    document.getElementById('timeSlots').innerHTML = '<p class="text-muted">Selecione uma data para ver os horários disponíveis</p>';
}

// Selecionar um dia
function selectDay(day, element) {
    selectedDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), day);
    selectedTime = null;
    document.getElementById('confirmBtn').disabled = true;

    // Atualizar seleção no calendário
    document.querySelectorAll('.calendar-day').forEach(dayEl => {
        dayEl.classList.remove('selected');
    });
    element.classList.add('selected');

    // Gerar horários disponíveis
    generateTimeSlots();
}

// Gerar horários disponíveis
function generateTimeSlots() {
    let timeSlotsHTML = '';

    // Horários baseados no hemocentro selecionado
    let slots = [];
    if (selectedLocation === 1) { // Hemocentro Regional
        if (selectedDate.getDay() === 6) { // Sábado
            slots = ["07:00", "08:00", "09:00", "10:00", "11:00"];
        } else { // Dias de semana
            slots = ["07:00", "08:00", "09:00", "10:00", "11:00", "14:00", "15:00", "16:00", "17:00"];
        }
    } else if (selectedLocation === 2) { // Hospital Santa Casa
        slots = ["08:00", "09:00", "10:00", "11:00", "14:00", "15:00", "16:00"];
    } else if (selectedLocation === 3) { // Unidade Móvel
        slots = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00"];
    }

    // Adicionar alguns horários indisponíveis (simulação)
    const unavailableSlots = ["09:00", "14:00"];

    timeSlotsHTML += '<div class="d-flex flex-wrap">';
    slots.forEach(slot => {
        const isUnavailable = unavailableSlots.includes(slot);
        timeSlotsHTML += `
                    <div class="time-slot ${isUnavailable ? 'unavailable' : ''} ${selectedTime === slot ? 'selected' : ''}" 
                         onclick="${isUnavailable ? '' : `selectTime('${slot}', this)`}">
                        ${slot}
                    </div>
                `;
    });
    timeSlotsHTML += '</div>';

    document.getElementById('timeSlots').innerHTML = timeSlotsHTML;
}

// Selecionar um horário
function selectTime(time, element) {
    selectedTime = time;
    document.getElementById('confirmBtn').disabled = false;

    // Atualizar seleção nos horários
    document.querySelectorAll('.time-slot').forEach(slot => {
        slot.classList.remove('selected');
    });
    element.classList.add('selected');
}

// Confirmar agendamento
function confirmAppointment() {
    if (!selectedLocation || !selectedDate || !selectedTime) {
        alert("Por favor, selecione um hemocentro, data e horário antes de confirmar.");
        return;
    }

    const locationName = locations[selectedLocation].name;
    const date = selectedDate.toLocaleDateString('pt-BR', { year: 'numeric', month: 'long', day: 'numeric' });
    const time = selectedTime;

    const appointmentDetails = `
                Hemocentro: ${locationName}
                Data: ${date}
                Horário: ${time}
            `;

    // Aqui você pode adicionar a lógica para enviar os dados do agendamento para o servidor
    // Exemplo: enviar para uma API ou salvar em um banco de dados

    // Para fins de demonstração, vamos apenas mostrar um alerta com os detalhes do agendamento
    alert(`Agendamento Confirmado!\n\n${appointmentDetails}`);

    // Redirecionar para a página de confirmação (opcional)
    // window.location.href = "pagina_confirmacao.html";
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.fade-in').forEach(function (el) {
        el.classList.add('visible');
    });
});