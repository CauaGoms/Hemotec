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
let currentDate = new Date(2025, 7, 1); // Agosto de 2025 (mês 7 = agosto)

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
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    let calendarHTML = '';
    
    // Gerar todas as semanas (6 semanas para cobrir todos os casos)
    for (let week = 0; week < 6; week++) {
        calendarHTML += '<div class="row calendar-week g-1 mb-1">';
        
        for (let dayOfWeek = 0; dayOfWeek < 7; dayOfWeek++) {
            const dayNumber = week * 7 + dayOfWeek - startingDay + 1;
            
            if (dayNumber <= 0 || dayNumber > daysInMonth) {
                // Dias vazios (mês anterior ou próximo)
                calendarHTML += '<div class="col"><div class="calendar-day-empty"></div></div>';
            } else {
                const dayDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), dayNumber);
                const dayNames = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];
                const dayName = dayNames[dayDate.getDay()];

                // Verificar disponibilidade baseada no hemocentro selecionado
                let isAvailable = true;
                let availabilityReason = '';
                
                if (selectedLocation === 3) { 
                    // Unidade móvel só funciona Ter e Qui
                    isAvailable = dayDate.getDay() === 2 || dayDate.getDay() === 4;
                    if (!isAvailable) availabilityReason = 'Unidade fechada';
                } else if (selectedLocation === 2) {
                    // Hospital Santa Casa não funciona nos fins de semana
                    isAvailable = dayDate.getDay() !== 0 && dayDate.getDay() !== 6;
                    if (!isAvailable) availabilityReason = 'Fim de semana';
                } else if (selectedLocation === 1) {
                    // Hemocentro Regional não funciona aos domingos
                    isAvailable = dayDate.getDay() !== 0;
                    if (!isAvailable) availabilityReason = 'Fechado aos domingos';
                }

                // Verificar se é uma data passada
                const isPast = dayDate < today;
                if (isPast) {
                    isAvailable = false;
                    availabilityReason = 'Data passada';
                }

                // Verificar se é hoje
                const isToday = dayDate.getTime() === today.getTime();
                
                // Verificar se está selecionado
                const isSelected = selectedDate && 
                    selectedDate.getDate() === dayNumber && 
                    selectedDate.getMonth() === currentDate.getMonth() &&
                    selectedDate.getFullYear() === currentDate.getFullYear();

                const dayClasses = [
                    'calendar-day',
                    isPast ? 'past' : '',
                    !isAvailable ? 'unavailable' : 'available',
                    isSelected ? 'selected' : '',
                    isToday ? 'today' : ''
                ].filter(Boolean).join(' ');

                const clickHandler = (isPast || !isAvailable) ? '' : `selectDay(${dayNumber}, this)`;

                calendarHTML += `
                    <div class="col">
                        <div class="${dayClasses}" 
                             onclick="${clickHandler}"
                             title="${!isAvailable ? availabilityReason : 'Clique para selecionar'}"
                             data-day="${dayNumber}">
                            <div class="day-number">${dayNumber}</div>
                            <div class="day-name">${dayName}</div>
                            ${isToday ? '<div class="today-indicator">•</div>' : ''}
                        </div>
                    </div>
                `;
            }
        }
        
        calendarHTML += '</div>';
        
        // Se chegamos ao final do mês e não precisamos de mais semanas, pare
        if (week * 7 + 7 - startingDay > daysInMonth) {
            break;
        }
    }

    document.getElementById('calendarDays').innerHTML = calendarHTML;
}

// Mudar mês
function changeMonth(direction) {
    const newDate = new Date(currentDate.getFullYear(), currentDate.getMonth() + direction, 1);
    const today = new Date();
    
    // Não permitir navegar para meses passados
    if (newDate.getFullYear() < today.getFullYear() || 
        (newDate.getFullYear() === today.getFullYear() && newDate.getMonth() < today.getMonth())) {
        return;
    }

    currentDate = newDate;
    updateCalendar();

    // Resetar seleções de data e horário se a data selecionada não estiver mais no mês atual
    if (selectedDate && 
        (selectedDate.getMonth() !== currentDate.getMonth() || 
         selectedDate.getFullYear() !== currentDate.getFullYear())) {
        selectedDate = null;
        selectedTime = null;
        document.getElementById('confirmBtn').disabled = true;
        document.getElementById('timeSlots').innerHTML = '<p class="text-muted">Selecione uma data para ver os horários disponíveis</p>';
    }
}

// Selecionar um dia
function selectDay(day, element) {
    // Verificar se o dia é válido e disponível
    if (!element || element.classList.contains('unavailable') || element.classList.contains('past')) {
        return;
    }

    selectedDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), day);
    selectedTime = null;
    document.getElementById('confirmBtn').disabled = true;

    // Remover seleção anterior
    document.querySelectorAll('.calendar-day').forEach(dayEl => {
        dayEl.classList.remove('selected');
    });
    
    // Adicionar seleção ao dia clicado
    element.classList.add('selected');

    // Scroll suave para a seção de horários
    const timeSlotsSection = document.querySelector('#timeSlots').parentElement;
    if (timeSlotsSection) {
        timeSlotsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

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
    const dateOptions = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    const formattedDate = selectedDate.toLocaleDateString('pt-BR', dateOptions);
    const time = selectedTime;

    const appointmentDetails = `
Detalhes do Agendamento:
━━━━━━━━━━━━━━━━━━━━━━
🏥 Local: ${locationName}
📅 Data: ${formattedDate}
🕐 Horário: ${time}
━━━━━━━━━━━━━━━━━━━━━━

✅ Seu agendamento foi confirmado!
📧 Você receberá um e-mail de confirmação em breve.
📱 Lembre-se de chegar 15 minutos antes do horário agendado.
    `;

    // Aqui você pode adicionar a lógica para enviar os dados do agendamento para o servidor
    // Exemplo: 
    // const appointmentData = {
    //     locationId: selectedLocation,
    //     date: selectedDate.toISOString().split('T')[0],
    //     time: selectedTime,
    //     userId: getCurrentUserId() // função para obter ID do usuário logado
    // };
    // 
    // fetch('/api/agendamentos', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify(appointmentData)
    // })
    // .then(response => response.json())
    // .then(data => {
    //     if (data.success) {
    //         // Redirecionar para página de confirmação
    //         window.location.href = `/agendamento/confirmacao/${data.agendamentoId}`;
    //     } else {
    //         alert('Erro ao confirmar agendamento: ' + data.message);
    //     }
    // })
    // .catch(error => {
    //     alert('Erro de conexão. Tente novamente.');
    // });

    // Para fins de demonstração, vamos apenas mostrar um alerta com os detalhes do agendamento
    alert(appointmentDetails);

    // Simular redirecionamento após confirmação
    // window.location.href = "confirmacao-agendamento.html";
}

// Inicializar a página
function initializePage() {
    // Adicionar animações de fade-in
    document.querySelectorAll('.fade-in').forEach(function (el) {
        el.classList.add('visible');
    });

    // Definir data inicial como o mês atual
    const today = new Date();
    currentDate = new Date(today.getFullYear(), today.getMonth(), 1);
    
    // Se já existe um hemocentro selecionado, atualizar o calendário
    if (selectedLocation) {
        updateCalendar();
    }
}

document.addEventListener('DOMContentLoaded', initializePage);