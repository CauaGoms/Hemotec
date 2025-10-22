// ====================================
// Variáveis Globais
// ====================================
let currentMonth = new Date().getMonth();
let currentYear = new Date().getFullYear();
let selectedLocation = null;
let selectedDates = new Set();
let selectedTimes = new Set();
let generatedSlots = [];
let existingSchedules = []; // Horários já cadastrados

// Feriados nacionais brasileiros de 2025 e 2026
const feriados = [
    '2025-01-01', '2025-02-24', '2025-02-25', '2025-04-18', '2025-04-21',
    '2025-05-01', '2025-06-19', '2025-09-07', '2025-10-12', '2025-11-02',
    '2025-11-15', '2025-11-20', '2025-12-25',
    '2026-01-01', '2026-02-16', '2026-02-17', '2026-04-03', '2026-04-21',
    '2026-05-01', '2026-06-04', '2026-09-07', '2026-10-12', '2026-11-02',
    '2026-11-15', '2026-11-20', '2026-12-25'
];

// ====================================
// Funções de Mensagens
// ====================================
function showErrorMessage(message, duration = 5000) {
    const container = document.getElementById('messageContainer') || createMessageContainer();

    const messageDiv = document.createElement('div');
    messageDiv.className = 'custom-message error-message';
    messageDiv.innerHTML = `
        <i class="fas fa-exclamation-circle me-2"></i>
        <span>${message}</span>
    `;

    container.appendChild(messageDiv);

    // Animar entrada
    setTimeout(() => messageDiv.classList.add('show'), 10);

    // Remover após duração
    setTimeout(() => {
        messageDiv.classList.remove('show');
        setTimeout(() => messageDiv.remove(), 300);
    }, duration);
}

function showSuccessMessage(message, duration = 5000) {
    const container = document.getElementById('messageContainer') || createMessageContainer();

    const messageDiv = document.createElement('div');
    messageDiv.className = 'custom-message success-message';
    messageDiv.innerHTML = `
        <i class="fas fa-check-circle me-2"></i>
        <span>${message}</span>
    `;

    container.appendChild(messageDiv);

    // Animar entrada
    setTimeout(() => messageDiv.classList.add('show'), 10);

    // Remover após duração
    setTimeout(() => {
        messageDiv.classList.remove('show');
        setTimeout(() => messageDiv.remove(), 300);
    }, duration);
}

function showWarningMessage(message, duration = 5000) {
    const container = document.getElementById('messageContainer') || createMessageContainer();

    const messageDiv = document.createElement('div');
    messageDiv.className = 'custom-message warning-message';
    messageDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle me-2"></i>
        <span>${message}</span>
    `;

    container.appendChild(messageDiv);

    // Animar entrada
    setTimeout(() => messageDiv.classList.add('show'), 10);

    // Remover após duração
    setTimeout(() => {
        messageDiv.classList.remove('show');
        setTimeout(() => messageDiv.remove(), 300);
    }, duration);
}

function createMessageContainer() {
    const container = document.createElement('div');
    container.id = 'messageContainer';
    container.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        z-index: 9999;
        display: flex;
        flex-direction: column;
        gap: 10px;
    `;
    document.body.appendChild(container);

    // Adicionar estilos CSS
    if (!document.getElementById('message-styles')) {
        const style = document.createElement('style');
        style.id = 'message-styles';
        style.textContent = `
            .custom-message {
                min-width: 300px;
                max-width: 500px;
                padding: 0.875rem 1.25rem;
                border-radius: 0.5rem;
                font-size: 0.9375rem;
                font-weight: 500;
                display: flex;
                align-items: center;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                opacity: 0;
                transform: translateX(100%);
                transition: all 0.3s ease;
            }
            
            .custom-message.show {
                opacity: 1;
                transform: translateX(0);
            }
            
            .custom-message i {
                font-size: 1.25rem;
            }
            
            .error-message {
                background-color: #f8d7da;
                color: #842029;
                border: 1px solid #f5c2c7;
            }
            
            .success-message {
                background-color: #d1e7dd;
                color: #0f5132;
                border: 1px solid #badbcc;
            }
            
            .warning-message {
                background-color: #fff3cd;
                color: #997404;
                border: 1px solid #ffecb5;
            }
        `;
        document.head.appendChild(style);
    }

    return container;
}

// ====================================
// Inicialização
// ====================================
document.addEventListener('DOMContentLoaded', function () {
    // Não pré-seleciona nenhuma unidade
    // O usuário precisa clicar em uma unidade para começar
    updateProgressBar();
});

// ====================================
// Funções de Seleção de Unidade
// ====================================
async function selectLocation(cod, element, nome) {
    selectedLocation = {
        cod: cod,
        nome: nome || element.dataset.nome
    };

    // Remove active de todos os cards
    document.querySelectorAll('.location-card').forEach(card => {
        card.classList.remove('active');
    });

    // Adiciona active ao card clicado
    if (element) {
        element.classList.add('active');
    }

    // Reseta as seleções ao trocar de unidade
    selectedDates.clear();
    selectedTimes.clear();
    existingSchedules = [];

    // Mostra conteúdo principal
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('selectedLocation').style.display = 'block';

    // Carrega horários já cadastrados
    await loadExistingSchedules(cod);

    // Renderiza calendário
    renderCalendar();
    updateSummary();
    updateProgressBar();
}

// Carrega os horários já cadastrados para a unidade
async function loadExistingSchedules(cod_unidade) {
    try {
        const response = await fetch(`/api/colaborador/disponibilidade-coleta/${cod_unidade}`);
        const data = await response.json();

        if (data.success) {
            existingSchedules = data.horarios || [];
            console.log(`${existingSchedules.length} horários já cadastrados para esta unidade`);
            renderExistingSchedules();
        }
    } catch (error) {
        console.error('Erro ao carregar horários existentes:', error);
        existingSchedules = [];
    }
}

// Renderiza a lista de horários já cadastrados
function renderExistingSchedules() {
    const section = document.getElementById('existingSchedulesSection');
    const list = document.getElementById('existingSchedulesList');
    const count = document.getElementById('existingSchedulesCount');

    if (!section || !list || !count) return;

    if (existingSchedules.length === 0) {
        section.style.display = 'none';
        return;
    }

    section.style.display = 'block';
    count.textContent = existingSchedules.length;

    // Scroll suave para a seção (após um pequeno delay)
    setTimeout(() => {
        section.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 300);

    // Agrupa horários por data
    const schedulesByDate = {};
    existingSchedules.forEach(schedule => {
        if (!schedulesByDate[schedule.data_agenda]) {
            schedulesByDate[schedule.data_agenda] = [];
        }
        schedulesByDate[schedule.data_agenda].push(schedule);
    });

    // Ordena as datas
    const sortedDates = Object.keys(schedulesByDate).sort();

    // Renderiza os horários
    list.innerHTML = '';
    sortedDates.forEach(date => {
        const schedules = schedulesByDate[date];
        const dateObj = new Date(date + 'T00:00:00');
        const formattedDate = dateObj.toLocaleDateString('pt-BR', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            weekday: 'short'
        });

        // Cria um único card por dia
        const dayCard = document.createElement('div');
        dayCard.className = 'schedule-day-card';

        // Cabeçalho do card com a data
        const header = document.createElement('div');
        header.className = 'schedule-day-header';
        header.innerHTML = `
            <i class="far fa-calendar me-2"></i>
            ${formattedDate}
            <span class="badge bg-primary ms-2">${schedules.length} horário${schedules.length > 1 ? 's' : ''}</span>
        `;
        dayCard.appendChild(header);

        // Lista de horários do dia
        const timesList = document.createElement('div');
        timesList.className = 'schedule-times-list';

        schedules.forEach(schedule => {
            const vagasDisponiveis = schedule.vagas - schedule.quantidade_doadores;
            const vagasColor = vagasDisponiveis > 0 ? 'success' : 'danger';

            const timeItem = document.createElement('div');
            timeItem.className = 'schedule-time-item';
            timeItem.innerHTML = `
                <div class="time-info">
                    <i class="far fa-clock me-2"></i>
                    <span class="time-value">${schedule.hora_agenda}</span>
                </div>
                <span class="badge bg-${vagasColor}">${vagasDisponiveis}/${schedule.vagas}</span>
            `;
            timesList.appendChild(timeItem);
        });

        dayCard.appendChild(timesList);
        list.appendChild(dayCard);
    });
}

// ====================================
// Funções de Calendário
// ====================================
function renderCalendar() {
    const calendarDays = document.getElementById('calendarDays');
    if (!calendarDays) return;

    calendarDays.innerHTML = '';

    const firstDay = new Date(currentYear, currentMonth, 1);
    const lastDay = new Date(currentYear, currentMonth + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDayOfWeek = firstDay.getDay();

    // Atualiza título do mês
    const monthNames = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
    document.getElementById('currentMonth').textContent = `${monthNames[currentMonth]} ${currentYear}`;

    // Adiciona células vazias antes do primeiro dia
    for (let i = 0; i < startingDayOfWeek; i++) {
        const emptyDay = document.createElement('div');
        emptyDay.classList.add('calendar-day', 'empty');
        calendarDays.appendChild(emptyDay);
    }

    // Adiciona os dias do mês
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    for (let day = 1; day <= daysInMonth; day++) {
        const date = new Date(currentYear, currentMonth, day);
        date.setHours(0, 0, 0, 0);
        const dateString = formatDate(date);

        const dayElement = document.createElement('div');
        dayElement.classList.add('calendar-day');
        dayElement.textContent = day;
        dayElement.dataset.date = dateString;

        // Desabilita dias passados
        if (date < today) {
            dayElement.classList.add('disabled');
        } else {
            // Verifica se é fim de semana ou feriado
            const dayOfWeek = date.getDay();
            const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;
            const isHoliday = feriados.includes(dateString);

            // Marca visualmente finais de semana e feriados, mas permite seleção
            if (isWeekend || isHoliday) {
                dayElement.classList.add('weekend');
                if (isHoliday) {
                    dayElement.title = 'Feriado';
                }
            }

            // Verifica se já existem horários cadastrados para este dia
            const hasExistingSchedule = existingSchedules.some(schedule => schedule.data_agenda === dateString);
            if (hasExistingSchedule) {
                dayElement.classList.add('has-schedule');
                const badge = document.createElement('span');
                badge.className = 'schedule-badge';
                badge.innerHTML = '<i class="fas fa-clock"></i>';
                dayElement.appendChild(badge);

                // Atualiza o tooltip
                const existingCount = existingSchedules.filter(s => s.data_agenda === dateString).length;
                const currentTitle = dayElement.title || '';
                dayElement.title = currentTitle ? `${currentTitle} - ${existingCount} horário(s) cadastrado(s)` : `${existingCount} horário(s) cadastrado(s)`;
            }

            // Mantém seleção anterior se existir
            if (selectedDates.has(dateString)) {
                dayElement.classList.add('selected');
            }

            // Adiciona evento de clique para todos os dias futuros
            dayElement.addEventListener('click', () => toggleDate(dateString, dayElement));
        }

        calendarDays.appendChild(dayElement);
    }

    updateSelectedDatesCount();
    updateToggleButtonText();
}

function updateToggleButtonText() {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

    // Pega todos os dias úteis (não finais de semana/feriados) do mês atual
    const calendarDays = document.querySelectorAll('#calendarDays .calendar-day:not(.disabled):not(.other-month):not(.weekend)');

    let allWeekdaysSelected = true;
    let hasEligibleWeekdays = false;

    calendarDays.forEach(dayElement => {
        const dateString = dayElement.dataset.date;
        if (dateString) {
            const dayDate = new Date(dateString);
            if (dayDate >= today) {
                hasEligibleWeekdays = true;
                if (!selectedDates.has(dateString)) {
                    allWeekdaysSelected = false;
                }
            }
        }
    });

    const toggleMonthTextElement = document.getElementById('toggleMonthText');
    if (toggleMonthTextElement) {
        if (allWeekdaysSelected && hasEligibleWeekdays) {
            toggleMonthTextElement.textContent = 'Desselecionar Mês Inteiro';
        } else {
            toggleMonthTextElement.textContent = 'Selecionar Mês Inteiro';
        }
    }
}

function toggleDate(dateString, element) {
    if (element.classList.contains('disabled')) return;

    if (selectedDates.has(dateString)) {
        selectedDates.delete(dateString);
        element.classList.remove('selected');
    } else {
        selectedDates.add(dateString);
        element.classList.add('selected');
    }

    updateSelectedDatesCount();
    updateSummary();
    updateProgressBar();
}

function changeMonth(direction) {
    currentMonth += direction;

    if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
    } else if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
    }

    renderCalendar();
}

function toggleMonthSelection() {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

    // Pega apenas os dias úteis do mês atual (exclui finais de semana e feriados)
    const weekdayElements = document.querySelectorAll('#calendarDays .calendar-day:not(.disabled):not(.other-month):not(.weekend)');

    // Verifica se todos os dias úteis elegíveis estão selecionados
    let allWeekdaysSelected = true;
    const eligibleWeekdays = [];

    weekdayElements.forEach(dayElement => {
        const dateString = dayElement.dataset.date;
        if (dateString) {
            const dayDate = new Date(dateString);
            // Só considera dias >= hoje e que não sejam finais de semana/feriados
            if (dayDate >= today) {
                eligibleWeekdays.push(dateString);
                if (!selectedDates.has(dateString)) {
                    allWeekdaysSelected = false;
                }
            }
        }
    });

    // Se todos os dias úteis estão selecionados, desseleciona; caso contrário, seleciona todos os dias úteis
    const toggleMonthTextElement = document.getElementById('toggleMonthText');

    if (allWeekdaysSelected && eligibleWeekdays.length > 0) {
        // Desselecionar todos os dias úteis
        eligibleWeekdays.forEach(dateString => {
            selectedDates.delete(dateString);
            const dayElement = document.querySelector(`[data-date="${dateString}"]`);
            if (dayElement) {
                dayElement.classList.remove('selected');
            }
        });
        toggleMonthTextElement.textContent = 'Selecionar Mês Inteiro';
    } else {
        // Selecionar todos os dias úteis
        eligibleWeekdays.forEach(dateString => {
            selectedDates.add(dateString);
            const dayElement = document.querySelector(`[data-date="${dateString}"]`);
            if (dayElement) {
                dayElement.classList.add('selected');
            }
        });
        toggleMonthTextElement.textContent = 'Desselecionar Mês Inteiro';
    }

    updateSelectedDatesCount();
    updateSummary();
    updateProgressBar();
}

function updateSelectedDatesCount() {
    document.getElementById('selectedDatesCount').textContent = `${selectedDates.size} selecionadas`;
}

// ====================================
// Funções de Horários
// ====================================
function selectWorkingHours() {
    document.getElementById('horaInicio').value = '08:00';
    document.getElementById('horaFim').value = '17:00';
}

function selectExtendedHours() {
    document.getElementById('horaInicio').value = '07:00';
    document.getElementById('horaFim').value = '19:00';
}

function clearTimeSelection() {
    selectedTimes.clear();
    document.getElementById('timeSlots').innerHTML = '<p class="empty-message">Configure e gere os horários acima</p>';
    updateSummary();
    updateProgressBar();
}

function gerarHorarios() {
    const horaInicio = document.getElementById('horaInicio').value;
    const horaFim = document.getElementById('horaFim').value;
    const intervalo = 30; // Fixo em 30 minutos
    const vagas = parseInt(document.getElementById('vagasHorario').value);

    if (!horaInicio || !horaFim) {
        showWarningMessage('Por favor, selecione o horário inicial e final.');
        return;
    }

    if (horaInicio >= horaFim) {
        showErrorMessage('O horário inicial deve ser anterior ao horário final.');
        return;
    }

    selectedTimes.clear();
    const timeSlotsContainer = document.getElementById('timeSlots');
    timeSlotsContainer.innerHTML = '';

    // Gera os horários
    let currentTime = horaInicio;

    while (currentTime < horaFim) {
        const timeSlot = document.createElement('div');
        timeSlot.classList.add('time-slot', 'selected');
        timeSlot.dataset.time = currentTime;
        timeSlot.dataset.vagas = vagas;

        timeSlot.innerHTML = `
            <div class="time-slot-content">
                <i class="fas fa-clock"></i>
                <span class="time-label">${currentTime}</span>
                <span class="badge bg-danger">${vagas} vagas</span>
            </div>
        `;

        timeSlot.addEventListener('click', () => toggleTimeSlot(currentTime, timeSlot));

        timeSlotsContainer.appendChild(timeSlot);
        selectedTimes.add(currentTime);

        // Adiciona o intervalo
        const [hours, minutes] = currentTime.split(':').map(Number);
        const totalMinutes = hours * 60 + minutes + intervalo;
        const newHours = Math.floor(totalMinutes / 60);
        const newMinutes = totalMinutes % 60;
        currentTime = `${String(newHours).padStart(2, '0')}:${String(newMinutes).padStart(2, '0')}`;
    }

    updateSummary();
    updateProgressBar();
}

function toggleTimeSlot(time, element) {
    if (selectedTimes.has(time)) {
        selectedTimes.delete(time);
        element.classList.remove('selected');
    } else {
        selectedTimes.add(time);
        element.classList.add('selected');
    }

    updateSummary();
    updateProgressBar();
}

// ====================================
// Funções de Resumo e Confirmação
// ====================================
function updateSummary() {
    const summarySection = document.getElementById('summarySection');
    const confirmBtn = document.getElementById('confirmBtn');

    const datesCount = selectedDates.size;
    const timesCount = selectedTimes.size;
    const vagas = parseInt(document.getElementById('vagasHorario').value) || 0;
    const totalSlots = datesCount * timesCount * vagas;

    document.getElementById('summaryDates').textContent = datesCount;
    document.getElementById('summaryTimes').textContent = timesCount;
    document.getElementById('summaryTotal').textContent = totalSlots;

    if (datesCount > 0 && timesCount > 0) {
        summarySection.style.display = 'block';
        confirmBtn.disabled = false;
    } else {
        summarySection.style.display = 'none';
        confirmBtn.disabled = true;
    }
}

async function confirmarDisponibilidade() {
    if (!selectedLocation || selectedDates.size === 0 || selectedTimes.size === 0) {
        showWarningMessage('Por favor, complete todas as seleções antes de confirmar.');
        return;
    }

    const confirmBtn = document.getElementById('confirmBtn');
    confirmBtn.disabled = true;
    confirmBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Salvando...';

    try {
        // Monta os agendamentos
        const agendamentos = [];
        const vagas = parseInt(document.getElementById('vagasHorario').value);

        for (const date of selectedDates) {
            for (const time of selectedTimes) {
                agendamentos.push({
                    cod_unidade: parseInt(selectedLocation.cod),
                    data_agenda: date,
                    hora_agenda: time + ':00',
                    vagas: vagas,
                    quantidade_doadores: 0
                });
            }
        }

        // Envia para a API
        const response = await fetch('/api/colaborador/disponibilidade-coleta', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                agendamentos: agendamentos
            })
        });

        const data = await response.json();

        if (data.success) {
            // Recarrega os horários cadastrados
            await loadExistingSchedules(selectedLocation.cod);

            // Atualiza o calendário para mostrar os novos badges
            renderCalendar();

            // Mostra mensagem de sucesso
            showSuccessMessage(data.message, 6000);

            // Reseta as seleções
            selectedDates.clear();
            selectedTimes.clear();
            document.getElementById('timeSlots').innerHTML = '<p class="empty-message">Configure e gere os horários acima</p>';
            updateSummary();
            updateProgressBar();

            // Mostra modal de sucesso
            setTimeout(() => {
                const successModal = new bootstrap.Modal(document.getElementById('successModal'));
                successModal.show();
            }, 500);
        } else {
            showErrorMessage('Erro ao salvar disponibilidade: ' + data.message);
            confirmBtn.disabled = false;
            confirmBtn.innerHTML = '<i class="fas fa-check-circle me-2"></i>Salvar Disponibilidades';
        }

    } catch (error) {
        console.error('Erro:', error);
        showErrorMessage('Erro ao processar requisição. Por favor, tente novamente.');
        confirmBtn.disabled = false;
        confirmBtn.innerHTML = '<i class="fas fa-check-circle me-2"></i>Salvar Disponibilidades';
    }
}

// ====================================
// Funções Auxiliares
// ====================================
function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

function updateProgressBar() {
    const steps = document.querySelectorAll('.progress-step');
    let currentStep = 1;

    if (selectedLocation) currentStep = 2;
    if (selectedDates.size > 0) currentStep = 3;
    if (selectedTimes.size > 0) currentStep = 4;

    steps.forEach((step, index) => {
        const stepNumber = index + 1;
        if (stepNumber <= currentStep) {
            step.classList.add('active');
        } else {
            step.classList.remove('active');
        }
    });
}
