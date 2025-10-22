// ====================================
// Variáveis Globais
// ====================================
let currentMonth = new Date().getMonth();
let currentYear = new Date().getFullYear();
let selectedLocation = null;
let selectedDates = new Set();
let selectedTimes = new Set();
let generatedSlots = [];

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
function selectLocation(cod, element, nome) {
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

    // Mostra conteúdo principal
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('selectedLocation').style.display = 'block';

    // Renderiza calendário
    renderCalendar();
    updateSummary();
    updateProgressBar();
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

            // Pré-seleciona TODOS OS DIAS ÚTEIS (exceto finais de semana e feriados)
            if (!isWeekend && !isHoliday) {
                selectedDates.add(dateString);
                dayElement.classList.add('selected');
            } else {
                // Marca finais de semana e feriados com estilo diferente
                dayElement.classList.add('weekend');
                if (isHoliday) {
                    dayElement.title = 'Feriado';
                }
            }

            dayElement.addEventListener('click', () => toggleDate(dateString, dayElement));
        }

        calendarDays.appendChild(dayElement);
    }

    updateSelectedDatesCount();
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
        alert('Por favor, selecione o horário inicial e final.');
        return;
    }

    if (horaInicio >= horaFim) {
        alert('O horário inicial deve ser anterior ao horário final.');
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
        alert('Por favor, complete todas as seleções antes de confirmar.');
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
            // Mostra modal de sucesso
            const successModal = new bootstrap.Modal(document.getElementById('successModal'));
            successModal.show();
        } else {
            alert('Erro ao salvar disponibilidade: ' + data.message);
            confirmBtn.disabled = false;
            confirmBtn.innerHTML = '<i class="fas fa-check-circle me-2"></i>Salvar Disponibilidades';
        }

    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao processar requisição. Por favor, tente novamente.');
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
