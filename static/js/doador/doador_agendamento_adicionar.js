/**
 * JavaScript para página de agendamento - Adicionar
 * Calcula distâncias e ordena unidades de coleta
 */

let selectedLocationId = null;
let selectedDate = null;
let selectedTime = null;
let userLocation = null;

// Função para calcular distância usando fórmula de Haversine
function calcularDistancia(lat1, lon1, lat2, lon2) {
    const R = 6371; // Raio da Terra em km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
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

    // Inicializa o calendário e busca datas disponíveis
    initCalendar();
    buscarDatasDisponiveis();

    console.log('Localização selecionada:', id);
}

async function buscarDatasDisponiveis() {
    if (!selectedLocationId) return;

    try {
        const response = await fetch(
            `/api/doador/agendamento/datas-disponiveis?cod_unidade=${selectedLocationId}&mes=${currentMonth + 1}&ano=${currentYear}`
        );

        if (!response.ok) {
            throw new Error('Erro ao buscar datas disponíveis');
        }

        const data = await response.json();

        if (data.success && data.datas) {
            // Armazena as datas disponíveis globalmente
            window.datasDisponiveis = new Set(data.datas);
            // Atualiza o calendário para refletir as datas disponíveis
            updateCalendar();
        }
    } catch (error) {
        console.error('Erro ao buscar datas disponíveis:', error);
    }
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

// Calendário e horários (mantido do código original)
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

        const dayDateString = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;

        // Desabilita dias passados
        if (dayDate < todayDate) {
            dayElement.classList.add('past');
            dayElement.classList.add('unavailable');
        }
        // Desabilita domingos
        else if (dayDate.getDay() === 0) {
            dayElement.classList.add('unavailable');
        }
        // Verifica se a data está nas datas disponíveis (se datasDisponiveis existe)
        else if (window.datasDisponiveis && !window.datasDisponiveis.has(dayDateString)) {
            dayElement.classList.add('unavailable');
        }
        // Dias disponíveis
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

    // Busca datas disponíveis do novo mês
    if (selectedLocationId) {
        buscarDatasDisponiveis();
    }
}

function selectDate(day, element) {
    selectedDate = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;

    // Remove seleção anterior
    document.querySelectorAll('.calendar-day').forEach(d => d.classList.remove('selected'));

    // Adiciona seleção
    element.classList.add('selected');

    // Busca horários disponíveis da API
    buscarHorariosDisponiveis();

    console.log('Data selecionada:', selectedDate);
}

async function buscarHorariosDisponiveis() {
    if (!selectedLocationId || !selectedDate) {
        console.error('Unidade ou data não selecionada');
        return;
    }

    const timeSlotsContainer = document.getElementById('timeSlots');
    timeSlotsContainer.innerHTML = '<p class="text-center">Carregando horários...</p>';

    try {
        const response = await fetch(
            `/api/doador/agendamento/horarios-disponiveis?cod_unidade=${selectedLocationId}&data=${selectedDate}`
        );

        if (!response.ok) {
            throw new Error('Erro ao buscar horários');
        }

        const data = await response.json();

        if (data.success && data.horarios && data.horarios.length > 0) {
            generateTimeSlotsFromAPI(data.horarios);
        } else {
            timeSlotsContainer.innerHTML = '<p class="text-muted text-center py-4">Nenhum horário disponível para esta data.</p>';
        }
    } catch (error) {
        console.error('Erro ao buscar horários:', error);
        timeSlotsContainer.innerHTML = '<p class="text-danger text-center py-4">Erro ao carregar horários. Tente novamente.</p>';
    }
}

function generateTimeSlotsFromAPI(horarios) {
    const timeSlotsContainer = document.getElementById('timeSlots');
    timeSlotsContainer.innerHTML = '';

    horarios.forEach(horario => {
        const timeSlot = document.createElement('button');
        timeSlot.className = 'time-slot';
        timeSlot.innerHTML = `
            <div>${horario.horario}</div>
            <small style="font-size: 0.75rem; color: #666;">${horario.vagas_disponiveis} vaga(s)</small>
        `;
        timeSlot.dataset.codAgenda = horario.cod_agenda;
        timeSlot.addEventListener('click', () => selectTime(horario.horario, horario.cod_agenda, timeSlot));
        timeSlotsContainer.appendChild(timeSlot);
    });
}

function selectTime(time, codAgenda, element) {
    selectedTime = time;
    window.selectedCodAgenda = codAgenda; // Armazena o cod_agenda globalmente

    // Remove seleção anterior
    document.querySelectorAll('.time-slot').forEach(t => t.classList.remove('selected'));

    // Adiciona seleção
    element.classList.add('selected');

    // Habilita botão de confirmação
    document.getElementById('confirmBtn').disabled = false;

    console.log('Horário selecionado:', selectedTime, 'Código da Agenda:', codAgenda);
}

async function confirmAppointment() {
    if (!selectedLocationId || !selectedDate || !selectedTime) {
        mostrarErro('Por favor, selecione o local, data e horário.');
        return;
    }

    if (!window.selectedCodAgenda) {
        mostrarErro('Erro: código da agenda não encontrado. Por favor, selecione o horário novamente.');
        return;
    }

    // Desabilita o botão para evitar cliques duplos
    const confirmBtn = document.getElementById('confirmBtn');
    const btnText = confirmBtn.querySelector('.btn-text');
    const btnOriginalText = btnText ? btnText.textContent : confirmBtn.textContent;
    confirmBtn.disabled = true;

    if (btnText) {
        btnText.textContent = 'Verificando...';
    } else {
        confirmBtn.textContent = 'Verificando...';
    }

    try {
        // Verifica se o usuário pode agendar
        const codUsuario = window.cod_usuario; // Variável global definida no template
        console.log('cod_usuario:', codUsuario, 'selectedDate:', selectedDate);

        if (!codUsuario) {
            mostrarErro('Erro: código do usuário não encontrado. Recarregue a página e tente novamente.');
            confirmBtn.disabled = false;
            if (btnText) {
                btnText.textContent = btnOriginalText;
            } else {
                confirmBtn.textContent = btnOriginalText;
            }
            return;
        }

        const response = await fetch(`/api/doador/agendamento/verificar-disponibilidade?cod_usuario=${codUsuario}&data=${selectedDate}`);
        console.log('Response status:', response.status, 'Response OK:', response.ok);

        const result = await response.json();

        // Debug: mostrar resultado da API
        console.log('Resultado da verificação:', result);

        // Verifica se a resposta foi bem-sucedida
        if (!result || result.pode_agendar === undefined) {
            mostrarErro('Erro ao verificar disponibilidade. Tente novamente.');
            confirmBtn.disabled = false;
            if (btnText) {
                btnText.textContent = btnOriginalText;
            } else {
                confirmBtn.textContent = btnOriginalText;
            }
            return;
        }

        if (!result.pode_agendar) {
            // Mostra erro de validação
            const mensagemErro = result.motivo || 'Não é possível realizar o agendamento no momento.';
            mostrarErro(mensagemErro);
            confirmBtn.disabled = false;
            if (btnText) {
                btnText.textContent = btnOriginalText;
            } else {
                confirmBtn.textContent = btnOriginalText;
            }
            return;
        }

        // Tudo OK, redireciona para página de confirmação
        const params = new URLSearchParams({
            unidade: selectedLocationId,
            data: selectedDate,
            horario: selectedTime,
            cod_agenda: window.selectedCodAgenda
        });

        window.location.href = `/doador/agendamento/adicionar/confirmacao?${params.toString()}`;
    } catch (error) {
        console.error('Erro ao verificar disponibilidade:', error);
        console.error('Detalhes do erro:', error.message, error.stack);
        mostrarErro(`Erro ao verificar disponibilidade: ${error.message || 'Tente novamente.'}`);
        confirmBtn.disabled = false;
        if (btnText) {
            btnText.textContent = btnOriginalText;
        } else {
            confirmBtn.textContent = btnOriginalText;
        }
    }
}

function mostrarErro(mensagem) {
    // Remove erros anteriores
    const errosAntigos = document.querySelectorAll('.alert-danger.erro-validacao');
    errosAntigos.forEach(erro => erro.remove());

    // Cria elemento de erro
    const erroDiv = document.createElement('div');
    erroDiv.className = 'alert alert-danger alert-dismissible fade show erro-validacao';
    erroDiv.role = 'alert';
    erroDiv.innerHTML = `
        <i class="fas fa-exclamation-circle me-2"></i>
        <strong>Atenção!</strong> ${mensagem}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    // Insere no topo da seção de seleção de horários ou do modal/container principal
    const timeSection = document.querySelector('.time-section') || document.querySelector('.container');
    if (timeSection) {
        timeSection.insertBefore(erroDiv, timeSection.firstChild);
        // Scroll suave até o erro
        erroDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    // Auto-remove após 8 segundos
    setTimeout(() => {
        erroDiv.remove();
    }, 8000);
}

// Inicialização quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    console.log('Página de agendamento carregada');

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
