/**
 * JavaScript para página de agendamento - Alterar (Colaborador)
 * Calcula distâncias e ordena unidades de coleta
 */

let selectedLocationId = null;
let selectedDate = null;
let selectedTime = null;
let userLocation = null;

// Obter ID do agendamento da URL
const pathParts = window.location.pathname.split('/');
const agendamentoId = pathParts[pathParts.length - 1];

// Função para calcular distância usando fórmula de Haversine
function calcularDistancia(lat1, lon1, lat2, lon2) {
    const R = 6371; // Raio da Terra em km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = 
        Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
        Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    const distancia = R * c;
    return distancia;
}

// Função para atualizar distâncias baseado na localização do usuário
function atualizarDistancias(userLat, userLon) {
    const locationCards = document.querySelectorAll('.location-card');
    const unidadesComDistancia = [];
    const RAIO_MAXIMO_KM = 50; // Raio máximo de 50km
    
    locationCards.forEach(card => {
        const lat = parseFloat(card.dataset.latitude);
        const lon = parseFloat(card.dataset.longitude);
        const nome = card.dataset.nome;
        const cod = card.dataset.cod;
        
        if (lat && lon) {
            const distancia = calcularDistancia(userLat, userLon, lat, lon);
            
            // Filtrar apenas unidades dentro do raio de 50km
            if (distancia <= RAIO_MAXIMO_KM) {
                const distanceBadge = card.querySelector('[data-distance-badge]');
                
                if (distanceBadge) {
                    distanceBadge.textContent = distancia.toFixed(1) + ' km';
                }
                
                unidadesComDistancia.push({
                    card: card,
                    distancia: distancia,
                    nome: nome,
                    cod: cod
                });
            } else {
                // Ocultar unidades fora do raio
                card.style.display = 'none';
            }
        }
    });
    
    // Ordenar por distância
    unidadesComDistancia.sort((a, b) => a.distancia - b.distancia);
    
    // Reorganizar os cards no DOM e exibir
    const locationList = document.getElementById('location-list');
    if (locationList) {
        unidadesComDistancia.forEach(item => {
            item.card.style.display = 'block'; // Mostrar card
            locationList.appendChild(item.card);
        });
    }
    
    // Exibir mensagem se nenhuma unidade dentro do raio
    if (unidadesComDistancia.length === 0) {
        const mensagem = document.createElement('p');
        mensagem.className = 'text-muted text-center py-4';
        mensagem.textContent = 'Nenhuma unidade de coleta encontrada em um raio de 50km da sua localização.';
        locationList.appendChild(mensagem);
    }
    
    console.log(`${unidadesComDistancia.length} unidades encontradas dentro de 50km. Distâncias atualizadas e ordenadas.`);
}

// Função para obter localização do usuário
function obterLocalizacaoUsuario() {
    if (!('geolocation' in navigator)) {
        console.warn('Geolocalização não suportada pelo navegador');
        // Se geolocalização não disponível, mostrar todas as unidades
        const locationCards = document.querySelectorAll('.location-card');
        locationCards.forEach(card => {
            card.style.display = 'block';
            const distanceBadge = card.querySelector('[data-distance-badge]');
            if (distanceBadge) {
                distanceBadge.textContent = 'N/A';
            }
        });
        return;
    }
    
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const { latitude, longitude } = position.coords;
            userLocation = { lat: latitude, lon: longitude };
            console.log('Localização obtida:', latitude, longitude);
            atualizarDistancias(latitude, longitude);
        },
        (error) => {
            console.error('Erro ao obter localização:', error);
            // Em caso de erro, mostrar todas as unidades sem filtro
            const locationCards = document.querySelectorAll('.location-card');
            locationCards.forEach(card => {
                card.style.display = 'block';
                const distanceBadge = card.querySelector('[data-distance-badge]');
                if (distanceBadge) {
                    distanceBadge.textContent = 'N/A';
                }
            });
        },
        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        }
    );
}

// Função para selecionar localização
function selectLocation(id, element) {
    selectedLocationId = id;
    
    // Remove seleção de todos os cards
    document.querySelectorAll('.location-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    // Adiciona seleção ao card clicado
    element.classList.add('selected');
    
    // Mostra a seção de seleção de data/hora
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('selectedLocation').style.display = 'block';
    
    // Inicializa o calendário
    initCalendar();
    
    console.log('Localização selecionada:', id);
}

// Função de busca/filtro de hemocentros
function setupSearchFilter() {
    const searchInput = document.querySelector('.search-box input');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const locationCards = document.querySelectorAll('.location-card');
        
        locationCards.forEach(card => {
            const nome = card.dataset.nome.toLowerCase();
            const endereco = card.querySelector('.detail-item')?.textContent.toLowerCase() || '';
            
            if (nome.includes(searchTerm) || endereco.includes(searchTerm)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}

// Função para botão de localização
function setupLocationButton() {
    const locationBtn = document.querySelector('.btn-outline-danger');
    if (!locationBtn) return;
    
    locationBtn.addEventListener('click', () => {
        obterLocalizacaoUsuario();
    });
}

// Calendário e horários
let currentDate = new Date();
let currentMonth = currentDate.getMonth();
let currentYear = currentDate.getFullYear();

function initCalendar() {
    updateCalendar();
}

function updateCalendar() {
    const monthNames = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
    
    document.getElementById('currentMonth').textContent = `${monthNames[currentMonth]} ${currentYear}`;
    
    const firstDay = new Date(currentYear, currentMonth, 1).getDay();
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
    const today = new Date();
    
    const calendarDays = document.getElementById('calendarDays');
    calendarDays.innerHTML = '';
    
    // Adiciona dias vazios antes do primeiro dia do mês
    for (let i = 0; i < firstDay; i++) {
        const emptyDay = document.createElement('div');
        emptyDay.className = 'calendar-day empty';
        calendarDays.appendChild(emptyDay);
    }
    
    // Adiciona os dias do mês
    for (let day = 1; day <= daysInMonth; day++) {
        const dayElement = document.createElement('div');
        dayElement.className = 'calendar-day';
        dayElement.textContent = day;
        
        const dayDate = new Date(currentYear, currentMonth, day);
        const todayDate = new Date();
        todayDate.setHours(0, 0, 0, 0);
        
        // Desabilita dias passados
        if (dayDate < todayDate) {
            dayElement.classList.add('past');
            dayElement.classList.add('unavailable');
        }
        // Desabilita domingos
        else if (dayDate.getDay() === 0) {
            dayElement.classList.add('unavailable');
        }
        // Dias disponíveis (segunda a sábado, não passados)
        else {
            dayElement.classList.add('available');
            dayElement.addEventListener('click', () => selectDate(day, dayElement));
        }
        
        // Marca o dia de hoje
        if (dayDate.getTime() === todayDate.getTime()) {
            dayElement.classList.add('today');
        }
        
        calendarDays.appendChild(dayElement);
    }
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
    
    updateCalendar();
}

function selectDate(day, element) {
    selectedDate = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    
    // Remove seleção anterior
    document.querySelectorAll('.calendar-day').forEach(d => d.classList.remove('selected'));
    
    // Adiciona seleção
    element.classList.add('selected');
    
    // Gera horários disponíveis
    generateTimeSlots();
    
    console.log('Data selecionada:', selectedDate);
}

function generateTimeSlots() {
    const timeSlotsContainer = document.getElementById('timeSlots');
    timeSlotsContainer.innerHTML = '';
    
    // Horários disponíveis (exemplo)
    const timeSlots = [
        '07:00', '07:30', '08:00', '08:30', '09:00', '09:30',
        '10:00', '10:30', '11:00', '11:30', '13:00', '13:30',
        '14:00', '14:30', '15:00', '15:30', '16:00', '16:30'
    ];
    
    timeSlots.forEach(time => {
        const timeSlot = document.createElement('button');
        timeSlot.className = 'time-slot';
        timeSlot.textContent = time;
        timeSlot.addEventListener('click', () => selectTime(time, timeSlot));
        timeSlotsContainer.appendChild(timeSlot);
    });
}

function selectTime(time, element) {
    selectedTime = time;
    
    // Remove seleção anterior
    document.querySelectorAll('.time-slot').forEach(t => t.classList.remove('selected'));
    
    // Adiciona seleção
    element.classList.add('selected');
    
    // Habilita botão de confirmação
    document.getElementById('confirmBtn').disabled = false;
    
    console.log('Horário selecionado:', selectedTime);
}

function confirmAppointment() {
    if (!selectedLocationId || !selectedDate || !selectedTime) {
        alert('Por favor, selecione o novo local, data e horário.');
        return;
    }
    
    // Monta os dados para envio
    const dataHora = `${selectedDate}T${selectedTime}:00`;
    
    // Envia requisição para atualizar agendamento
    fetch(`/api/colaborador/agendamento/alterar/${agendamentoId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            local_agendamento: selectedLocationId,
            data_hora: dataHora
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Agendamento alterado com sucesso!');
            window.location.href = '/colaborador/agendamento';
        } else {
            alert('Erro ao alterar agendamento: ' + (data.message || 'Erro desconhecido'));
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao alterar agendamento. Por favor, tente novamente.');
    });
}

// Inicialização quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    console.log('Página de alteração de agendamento carregada');
    
    // Tenta obter localização automaticamente
    setTimeout(() => {
        obterLocalizacaoUsuario();
    }, 500);
    
    // Configura busca/filtro
    setupSearchFilter();
    
    // Configura botão de localização
    setupLocationButton();
    
    // Desabilita botão de confirmação inicialmente
    const confirmBtn = document.getElementById('confirmBtn');
    if (confirmBtn) {
        confirmBtn.disabled = true;
    }
});
