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
let currentDate = new Date(); // Inicializa com a data atual
let datasDisponiveisNoMes = []; // Armazena os dias do mês que têm horários disponíveis

// Atualizar indicador de progresso
function updateProgressStep(step) {
    document.querySelectorAll('.progress-step').forEach((stepEl, index) => {
        if (index + 1 <= step) {
            stepEl.classList.add('active');
        } else {
            stepEl.classList.remove('active');
        }
    });
}

// Selecionar um hemocentro
function selectLocation(locationId, element) {
    selectedLocation = locationId;

    // Atualizar a lista de hemocentros
    document.querySelectorAll('.location-card').forEach(card => {
        card.classList.remove('selected');
    });
    element.classList.add('selected');

    // Atualizar indicador de progresso
    updateProgressStep(2);

    // Mostrar seção de agendamento
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('selectedLocation').style.display = 'block';

    // Atualizar o calendário
    updateCalendar();

    // Resetar seleções de data e horário
    selectedDate = null;
    selectedTime = null;
    document.getElementById('confirmBtn').disabled = true;
    document.getElementById('confirmBtn').classList.add('disabled');
    document.getElementById('timeSlots').innerHTML = '<p class="empty-message">Selecione uma data para ver os horários disponíveis</p>';

    // Scroll suave para a seção de agendamento
    document.getElementById('selectedLocation').scrollIntoView({ behavior: 'smooth' });
}

// Atualizar o calendário
async function updateCalendar() {
    const monthNames = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
    document.getElementById('currentMonth').textContent = `${monthNames[currentDate.getMonth()]} ${currentDate.getFullYear()}`;

    // Buscar datas disponíveis da API se houver unidade selecionada
    if (selectedLocation) {
        try {
            const mes = currentDate.getMonth() + 1; // JavaScript usa 0-11, API usa 1-12
            const ano = currentDate.getFullYear();
            console.log(`Buscando datas disponíveis: unidade=${selectedLocation}, mes=${mes}, ano=${ano}`);
            const response = await fetch(`/api/agenda/datas-disponiveis?cod_unidade=${selectedLocation}&mes=${mes}&ano=${ano}`);
            const data = await response.json();
            console.log('Datas disponíveis recebidas:', data);

            if (data.success) {
                datasDisponiveisNoMes = data.datas;
                console.log('Dias disponíveis no mês:', datasDisponiveisNoMes);
            } else {
                datasDisponiveisNoMes = [];
            }
        } catch (error) {
            console.error('Erro ao buscar datas disponíveis:', error);
            datasDisponiveisNoMes = [];
        }
    } else {
        console.log('Nenhuma unidade selecionada');
        datasDisponiveisNoMes = [];
    }

    const firstDay = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
    const lastDay = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDay = firstDay.getDay();
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    let calendarHTML = '';

    // Gerar todas as semanas (6 semanas para cobrir todos os casos)
    for (let week = 0; week < 6; week++) {
        for (let dayOfWeek = 0; dayOfWeek < 7; dayOfWeek++) {
            const dayNumber = week * 7 + dayOfWeek - startingDay + 1;

            if (dayNumber <= 0 || dayNumber > daysInMonth) {
                // Dias vazios (mês anterior ou próximo)
                calendarHTML += '<div class="calendar-day-empty"></div>';
            } else {
                const dayDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), dayNumber);

                // Verificar se a data está na lista de datas disponíveis da API
                const isAvailable = datasDisponiveisNoMes.includes(dayNumber);

                // Verificar se é uma data passada
                const isPast = dayDate < today;

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

                let titleText = 'Clique para selecionar';
                if (isPast) {
                    titleText = 'Data passada';
                } else if (!isAvailable) {
                    titleText = 'Sem horários disponíveis';
                }

                calendarHTML += `
                    <div class="${dayClasses}" 
                         onclick="${clickHandler}"
                         title="${titleText}"
                         data-day="${dayNumber}">
                        ${dayNumber}
                        ${isToday ? '<div class="today-indicator">•</div>' : ''}
                    </div>
                `;
            }
        }

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
        updateProgressStep(2);
        document.getElementById('confirmBtn').disabled = true;
        document.getElementById('confirmBtn').classList.add('disabled');
        document.getElementById('timeSlots').innerHTML = '<p class="empty-message">Selecione uma data para ver os horários disponíveis</p>';
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

    // Atualizar indicador de progresso
    updateProgressStep(3);

    document.getElementById('confirmBtn').disabled = true;
    document.getElementById('confirmBtn').classList.add('disabled');

    // Remover seleção anterior
    document.querySelectorAll('.calendar-day').forEach(dayEl => {
        dayEl.classList.remove('selected');
    });

    // Adicionar seleção ao dia clicado
    element.classList.add('selected');

    // Scroll suave para a seção de horários
    const timeSlotsSection = document.querySelector('.time-section');
    if (timeSlotsSection) {
        timeSlotsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    // Gerar horários disponíveis
    generateTimeSlots();
}

// Gerar horários disponíveis
async function generateTimeSlots() {
    const timeSlotsContainer = document.getElementById('timeSlots');
    timeSlotsContainer.innerHTML = '<p class="empty-message">Carregando horários...</p>';

    if (!selectedDate || !selectedLocation) {
        timeSlotsContainer.innerHTML = '<p class="empty-message">Selecione uma data para ver os horários disponíveis</p>';
        return;
    }

    try {
        // Formatar data no formato YYYY-MM-DD
        const ano = selectedDate.getFullYear();
        const mes = String(selectedDate.getMonth() + 1).padStart(2, '0');
        const dia = String(selectedDate.getDate()).padStart(2, '0');
        const dataFormatada = `${ano}-${mes}-${dia}`;

        console.log(`Buscando horários: unidade=${selectedLocation}, data=${dataFormatada}`);

        // Buscar horários disponíveis da API
        const response = await fetch(`/api/agenda/horarios-disponiveis?cod_unidade=${selectedLocation}&data=${dataFormatada}`);
        const data = await response.json();
        console.log('Horários recebidos:', data);

        if (!data.success || !data.data || data.data.length === 0) {
            console.log('Nenhum horário disponível');
            timeSlotsContainer.innerHTML = '<p class="empty-message">Nenhum horário disponível para esta data</p>';
            return;
        }

        // Renderizar horários disponíveis
        let timeSlotsHTML = '';
        data.data.forEach(horario => {
            const isSelected = selectedTime === horario.hora;
            timeSlotsHTML += `
                <div class="time-slot ${isSelected ? 'selected' : ''}" 
                     onclick="selectTime('${horario.hora}', this)"
                     data-cod-agenda="${horario.cod_agenda}"
                     title="${horario.disponiveis} vaga(s) disponível(eis)">
                    ${horario.hora}
                    <small class="vagas-info">${horario.disponiveis}/${horario.vagas}</small>
                </div>
            `;
        });

        timeSlotsContainer.innerHTML = timeSlotsHTML;

    } catch (error) {
        console.error('Erro ao buscar horários disponíveis:', error);
        timeSlotsContainer.innerHTML = '<p class="empty-message">Erro ao carregar horários. Tente novamente.</p>';
    }
}

// Selecionar um horário
function selectTime(time, element) {
    selectedTime = time;

    // Atualizar indicador de progresso
    updateProgressStep(4);

    document.getElementById('confirmBtn').disabled = false;
    document.getElementById('confirmBtn').classList.remove('disabled');

    // Atualizar seleção nos horários
    document.querySelectorAll('.time-slot').forEach(slot => {
        slot.classList.remove('selected');
    });
    element.classList.add('selected');
}

// Confirmar agendamento
function confirmAppointment() {
    // Por enquanto, vamos redirecionar diretamente para a página de confirmação
    window.location.href = "/doador/agendamento/adicionar/confirmacao";
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

// Expor funções ao escopo global para permitir override em páginas específicas
window.selectLocation = selectLocation;
window.selectDay = selectDay;
window.selectTime = selectTime;
window.confirmAppointment = confirmAppointment;