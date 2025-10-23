let compatModalInstance = null;
// Mensagens de compatibilidade por tipo sanguíneo
const compatibilidadeSangue = {
    'A+': 'A+ pode receber de A+, A-, O+ e O-. Pode doar para A+ e AB+',
    'A-': 'A- pode receber de A- e O-. Pode doar para A+, A-, AB+ e AB-',
    'B+': 'B+ pode receber de B+, B-, O+ e O-. Pode doar para B+ e AB+',
    'B-': 'B- pode receber de B- e O-. Pode doar para B+, B-, AB+ e AB-',
    'AB+': 'AB+ pode receber de todos os tipos. Pode doar apenas para AB+',
    'AB-': 'AB- pode receber de AB-, A-, B- e O-. Pode doar para AB+ e AB-',
    'O+': 'O+ pode receber de O+ e O-. Pode doar para O+, A+, B+ e AB+',
    'O-': 'O- pode receber apenas de O-. Pode doar para todos os tipos.',
};


function mostrarCompatibilidade(tipo) {
    const msg = compatibilidadeSangue[tipo] || 'Tipo sanguíneo não encontrado.';
    // Quebra a mensagem em partes para melhor formatação
    let recebe = '';
    let doa = '';
    if (msg.includes('pode receber de')) {
        const partes = msg.split('Pode doar para');
        recebe = partes[0].replace('pode receber de', '').replace('Pode', '').trim();
        doa = (partes[1] || '').replace('.', '').trim();
    }
    const html = `<div style="text-align:center;">
        <div style="font-size:1.3rem;font-weight:700;color:#e02020;">${tipo}</div>
        <div style="margin-top:1rem;">
            <span style="font-weight:600;color:#333;">Recebe de:</span><br>
            <span style="color:#555;">${recebe}</span>
        </div>
        <div style="margin-top:1rem;">
            <span style="font-weight:600;color:#333;">Dá para:</span><br>
            <span style="color:#555;">${doa}</span>
        </div>
    </div>`;
    document.getElementById('compatModalBody').innerHTML = html;
    if (!compatModalInstance) {
        compatModalInstance = new bootstrap.Modal(document.getElementById('compatModal'));
    }
    compatModalInstance.show();
}

(function () {
    // Config das unidades será carregado dinamicamente do backend
    fetch('/api/unidades')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar dados da API: ' + response.statusText);
            }
            return response.json();
        })
        .then(unidades => {
            if (!Array.isArray(unidades) || unidades.length === 0) {
                console.error('Nenhuma unidade encontrada ou formato inválido.');
                return;
            }

            const mapa = L.map('mapa', { zoomControl: true, attributionControl: true })
                .setView([-20.851136957150032, -41.113483188824155], 11); // Coordenadas iniciais

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: '© OpenStreetMap'
            }).addTo(mapa);

            const statusEl = document.getElementById('geo-status');
            const infoRota = document.getElementById('info-rota');
            const btnLocate = document.getElementById('btn-locate');
            const btnClear = document.getElementById('btn-clear-route');
            const listaUnidades = document.getElementById('lista-unidades');

            let userMarker = null;
            let routingControl = null;

            function listarUnidades(unidadesParaMostrar = null) {
                if (!listaUnidades) return;
                listaUnidades.innerHTML = '';

                const unidadesAMostrar = unidadesParaMostrar || unidades;

                unidadesAMostrar.forEach(u => {
                    const { cod_unidade, nome, latitude: lat, longitude: lng, isCritica } = u;

                    const li = document.createElement('li');

                    let nomeExibicao = nome;
                    if (isCritica) {
                        nomeExibicao += ' ⚠️';
                    }

                    li.innerHTML = '<strong>' + nomeExibicao + '</strong><span>Coordenadas: ' + lat + ', ' + lng + '</span>';
                    const btn = document.createElement('button');
                    btn.type = 'button';
                    btn.textContent = 'Rota';
                    btn.classList.add('btn-rota');
                    btn.addEventListener('click', () => {
                        if (!userMarker) {
                            statusEl.textContent = 'Obtenha sua localização primeiro.';
                            return;
                        }
                        criarRota([userMarker.getLatLng().lat, userMarker.getLatLng().lng], [lat, lng], nome);
                        // Buscar estoque da unidade selecionada
                        fetch(`/api/estoque/${cod_unidade}`)
                            .then(resp => resp.json())
                            .then(resposta => {
                                const nomeUnidadeEl = document.getElementById('nome-unidade-estoque');
                                nomeUnidadeEl.textContent = `- ${nome}`;
                                nomeUnidadeEl.classList.remove('text-muted');
                                nomeUnidadeEl.classList.add('text-danger');

                                let estoqueObj = resposta.estoque;
                                if (typeof estoqueObj === 'string') {
                                    try { estoqueObj = JSON.parse(estoqueObj); } catch { }
                                }
                                if (estoqueObj) {
                                    renderizarEstoque(normalizarEstoque(estoqueObj));
                                } else {
                                    renderizarEstoque({});
                                }
                            })
                            .catch(() => {
                                document.getElementById('nome-unidade-estoque').textContent = '- Erro ao buscar estoque';
                            });
                    });
                    li.appendChild(btn);
                    listaUnidades.appendChild(li);
                });
            }

            // Função para listar unidades na seção de estoque
            function listarUnidadesEstoque(unidadesParaMostrar = null) {
                const listaEstoque = document.getElementById('lista-unidades-estoque');
                if (!listaEstoque) return;

                const unidadesAMostrar = unidadesParaMostrar || unidades;

                listaEstoque.innerHTML = '';
                unidadesAMostrar.forEach(u => {
                    const { cod_unidade, nome, isCritica } = u;

                    const li = document.createElement('li');
                    li.className = 'unidade-estoque-item';

                    let nomeExibicao = nome;
                    if (isCritica) {
                        nomeExibicao += ' ⚠️';
                    }

                    li.innerHTML = `
                        <div class="unidade-estoque-nome">${nomeExibicao}</div>
                    `;

                    li.addEventListener('click', () => {
                        // Remove active de todos os items
                        document.querySelectorAll('.unidade-estoque-item').forEach(item => {
                            item.classList.remove('active');
                        });
                        // Adiciona active no item clicado
                        li.classList.add('active');

                        // Buscar estoque da unidade selecionada
                        fetch(`/api/estoque/${cod_unidade}`)
                            .then(resp => resp.json())
                            .then(resposta => {
                                const nomeUnidadeEl = document.getElementById('nome-unidade-estoque');
                                nomeUnidadeEl.textContent = `- ${nome}`;
                                nomeUnidadeEl.classList.remove('text-muted');
                                nomeUnidadeEl.classList.add('text-danger');

                                let estoqueObj = resposta.estoque;
                                if (typeof estoqueObj === 'string') {
                                    try { estoqueObj = JSON.parse(estoqueObj); } catch { }
                                }
                                if (estoqueObj) {
                                    renderizarEstoque(normalizarEstoque(estoqueObj));
                                } else {
                                    renderizarEstoque({});
                                }

                                // Scroll suave para o estoque
                                document.getElementById('estoque-atual').scrollIntoView({
                                    behavior: 'smooth',
                                    block: 'nearest'
                                });
                            })
                            .catch(() => {
                                const nomeUnidadeEl = document.getElementById('nome-unidade-estoque');
                                nomeUnidadeEl.textContent = '- Erro ao buscar estoque';
                                nomeUnidadeEl.style.display = 'inline';
                            });
                    });

                    listaEstoque.appendChild(li);
                });
            }

            const unidadeIcon = L.icon({
                iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
                iconSize: [25, 41],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
                shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
                shadowSize: [41, 41]
            });

            // Criar marcadores para todas as unidades
            unidades.forEach(u => {
                const { cod_unidade, nome, latitude: lat, longitude: lng } = u;
                const m = L.marker([lat, lng], { icon: unidadeIcon }).addTo(mapa);
                m.bindPopup(`<strong>${nome}</strong><br>Coordenadas: ${lat}, ${lng}`);
            });

            // Função para buscar as 2 unidades com estoque mais crítico
            async function buscarUnidadesMaisCriticas(quantidade = 2) {
                try {
                    // Buscar estoque de todas as unidades
                    const promessas = unidades.map(u =>
                        fetch(`/api/estoque/${u.cod_unidade}`)
                            .then(resp => resp.json())
                            .then(resposta => ({
                                ...u,
                                estoque: resposta.estoque
                            }))
                            .catch(() => ({ ...u, estoque: {} }))
                    );

                    const unidadesComEstoque = await Promise.all(promessas);

                    // Calcular criticidade de cada unidade (soma de tipos críticos e baixos)
                    const unidadesComCriticidade = unidadesComEstoque.map(unidade => {
                        let pontosCriticidade = 0;
                        let estoqueObj = unidade.estoque || {};

                        // Normalizar se for string
                        if (typeof estoqueObj === 'string') {
                            try { estoqueObj = JSON.parse(estoqueObj); } catch { estoqueObj = {}; }
                        }

                        // Pontuar baseado na quantidade de cada tipo sanguíneo
                        Object.values(estoqueObj).forEach(item => {
                            const qtd = item.quantidade || 0;
                            if (qtd <= 59) pontosCriticidade += 10; // Crítico
                            else if (qtd <= 99) pontosCriticidade += 5; // Baixo
                            else if (qtd <= 149) pontosCriticidade += 2; // Moderado
                        });

                        return {
                            ...unidade,
                            criticidade: pontosCriticidade,
                            isCritica: pontosCriticidade > 0
                        };
                    });

                    // Ordenar por criticidade (maior primeiro)
                    unidadesComCriticidade.sort((a, b) => b.criticidade - a.criticidade);

                    // Retornar as N mais críticas
                    return unidadesComCriticidade.slice(0, quantidade);
                } catch (error) {
                    console.error('Erro ao buscar unidades mais críticas:', error);
                    return unidades.slice(0, quantidade); // Fallback
                }
            }

            function obterLocalizacao() {
                if (!('geolocation' in navigator)) {
                    statusEl.textContent = 'Geolocalização não suportada. Exibindo unidades com estoque mais crítico...';
                    buscarUnidadesMaisCriticas(2).then(unidadesCriticas => {
                        if (unidadesCriticas && unidadesCriticas.length > 0) {
                            // Atualizar ambas as listas com unidades críticas
                            listarUnidades(unidadesCriticas);
                            listarUnidadesEstoque(unidadesCriticas);

                            // Mostrar estoque da primeira unidade mais crítica
                            const unidade = unidadesCriticas[0];
                            const nomeUnidadeEl = document.getElementById('nome-unidade-estoque');
                            nomeUnidadeEl.textContent = `- ${unidade.nome} (Estoque Crítico)`;
                            nomeUnidadeEl.classList.remove('text-muted');
                            nomeUnidadeEl.classList.add('text-danger');

                            let estoqueObj = unidade.estoque;
                            if (typeof estoqueObj === 'string') {
                                try { estoqueObj = JSON.parse(estoqueObj); } catch { }
                            }
                            if (estoqueObj) {
                                renderizarEstoque(normalizarEstoque(estoqueObj));
                            }

                            statusEl.textContent = 'Exibindo unidades com maior necessidade de doações.';
                        }
                    });
                    return;
                }
                statusEl.textContent = 'Obtendo localização...';
                navigator.geolocation.getCurrentPosition(pos => {
                    const { latitude, longitude } = pos.coords;
                    statusEl.textContent = 'Localização obtida.';
                    if (userMarker) {
                        userMarker.setLatLng([latitude, longitude]);
                    } else {
                        userMarker = L.marker([latitude, longitude], {
                            icon: L.icon({
                                iconUrl: 'https://maps.gstatic.com/mapfiles/ms2/micons/man.png',
                                iconSize: [32, 32],
                                iconAnchor: [16, 32]
                            })
                        }).addTo(mapa).bindPopup('Você está aqui.').openPopup();
                    }
                    mapa.flyTo([latitude, longitude], 13, { duration: 0.8 });

                    // Encontrar as 2 unidades mais próximas
                    const unidadesComDistancia = unidades.map(u => {
                        const { cod_unidade, nome, latitude: lat, longitude: lng } = u;
                        const dist = Math.sqrt(Math.pow(lat - latitude, 2) + Math.pow(lng - longitude, 2));
                        return { ...u, distancia: dist };
                    });

                    // Ordenar por distância e pegar as 2 mais próximas
                    unidadesComDistancia.sort((a, b) => a.distancia - b.distancia);
                    const duasMaisProximas = unidadesComDistancia.slice(0, 2);

                    // Atualizar ambas as listas com as 2 mais próximas
                    listarUnidades(duasMaisProximas);
                    listarUnidadesEstoque(duasMaisProximas);

                    // Buscar e mostrar estoque da unidade mais próxima
                    if (duasMaisProximas.length > 0) {
                        const unidadeMaisProxima = duasMaisProximas[0];
                        fetch(`/api/estoque/${unidadeMaisProxima.cod_unidade}`)
                            .then(resp => resp.json())
                            .then(resposta => {
                                const nomeUnidadeEl = document.getElementById('nome-unidade-estoque');
                                nomeUnidadeEl.textContent = `- ${unidadeMaisProxima.nome}`;
                                nomeUnidadeEl.classList.remove('text-muted');
                                nomeUnidadeEl.classList.add('text-danger');

                                let estoqueObj = resposta.estoque;
                                if (typeof estoqueObj === 'string') {
                                    try { estoqueObj = JSON.parse(estoqueObj); } catch { }
                                }
                                if (estoqueObj) {
                                    renderizarEstoque(normalizarEstoque(estoqueObj));
                                } else {
                                    renderizarEstoque({});
                                }
                            })
                            .catch(() => {
                                document.getElementById('nome-unidade-estoque').textContent = '- Erro ao buscar estoque';
                            });
                    }
                }, err => {
                    statusEl.textContent = 'Localização não disponível. Exibindo unidades com estoque mais crítico...';
                    // Se falhar a localização, buscar as 2 unidades mais críticas
                    buscarUnidadesMaisCriticas(2).then(unidadesCriticas => {
                        if (unidadesCriticas && unidadesCriticas.length > 0) {
                            // Atualizar ambas as listas com unidades críticas
                            listarUnidades(unidadesCriticas);
                            listarUnidadesEstoque(unidadesCriticas);

                            // Mostrar estoque da primeira unidade mais crítica
                            const unidade = unidadesCriticas[0];
                            const nomeUnidadeEl = document.getElementById('nome-unidade-estoque');
                            nomeUnidadeEl.textContent = `- ${unidade.nome} (Estoque Crítico)`;
                            nomeUnidadeEl.classList.remove('text-muted');
                            nomeUnidadeEl.classList.add('text-danger');

                            let estoqueObj = unidade.estoque;
                            if (typeof estoqueObj === 'string') {
                                try { estoqueObj = JSON.parse(estoqueObj); } catch { }
                            }
                            if (estoqueObj) {
                                renderizarEstoque(normalizarEstoque(estoqueObj));
                            }

                            statusEl.textContent = 'Exibindo unidades com maior necessidade de doações.';
                        }
                    });
                }, { enableHighAccuracy: true, timeout: 10000 });
            }

            function criarRota(origem, destino, nome) {
                if (routingControl) {
                    mapa.removeControl(routingControl);
                    routingControl = null;
                }
                routingControl = L.Routing.control({
                    waypoints: [
                        L.latLng(origem[0], origem[1]),
                        L.latLng(destino[0], destino[1])
                    ],
                    lineOptions: {
                        styles: [{ color: '#dc3545', weight: 5, opacity: 0.85 }]
                    },
                    show: false,
                    addWaypoints: false,
                    draggableWaypoints: false,
                    fitSelectedRoutes: true,
                    routeWhileDragging: false,
                    language: 'pt-BR'
                }).addTo(mapa);

                routingControl.on('routesfound', e => {
                    const r = e.routes[0];
                    const distKm = (r.summary.totalDistance / 1000).toFixed(2);
                    const durMin = Math.round(r.summary.totalTime / 60);
                    infoRota.innerHTML = '<strong>Rota até ' + nome + '</strong><br>Distância: ' + distKm + ' km<br>Tempo estimado: ' + durMin + ' min';
                    btnClear.disabled = false;
                });

                routingControl.on('routingerror', () => {
                    infoRota.innerHTML = 'Falha ao calcular rota.';
                    btnClear.disabled = false;
                });
            }

            if (btnLocate) btnLocate.addEventListener('click', obterLocalizacao);
            if (btnClear) btnClear.addEventListener('click', () => {
                if (routingControl) {
                    mapa.removeControl(routingControl);
                    routingControl = null;
                }
                infoRota.innerHTML = '';
                btnClear.disabled = true;
            });

            // Auto tentar localização se seguro (localhost ou https)
            if (location.protocol === 'https:' || location.hostname === 'localhost' || location.hostname === '127.0.0.1') {
                setTimeout(() => obterLocalizacao(), 600);
            } else {
                statusEl.textContent = 'Buscando unidades com estoque mais crítico...';
                // Se não puder usar geolocalização, buscar as 2 unidades mais críticas
                buscarUnidadesMaisCriticas(2).then(unidadesCriticas => {
                    if (unidadesCriticas && unidadesCriticas.length > 0) {
                        // Atualizar ambas as listas com unidades críticas
                        listarUnidades(unidadesCriticas);
                        listarUnidadesEstoque(unidadesCriticas);

                        // Mostrar estoque da primeira unidade mais crítica
                        const unidade = unidadesCriticas[0];
                        const nomeUnidadeEl = document.getElementById('nome-unidade-estoque');
                        nomeUnidadeEl.textContent = `- ${unidade.nome} (Estoque Crítico)`;
                        nomeUnidadeEl.classList.remove('text-muted');
                        nomeUnidadeEl.classList.add('text-danger');

                        let estoqueObj = unidade.estoque;
                        if (typeof estoqueObj === 'string') {
                            try { estoqueObj = JSON.parse(estoqueObj); } catch { }
                        }
                        if (estoqueObj) {
                            renderizarEstoque(normalizarEstoque(estoqueObj));
                        }
                        statusEl.textContent = 'Exibindo unidades com maior necessidade de doações.';
                    }
                });
            }
        })
        .catch(error => {
            console.error('Erro ao carregar unidades:', error);
        });
})();

// Função para renderizar o estoque visualmente
function renderizarEstoque(estoque) {
    const estoqueEl = document.getElementById('estoque-atual');
    if (!estoqueEl) return;
    if (!estoque || Object.keys(estoque).length === 0) {
        estoqueEl.innerHTML = '';
        return;
    }
    // Estrutura visual igual aos cards antigos
    let html = '';
    const statusMap = {
        'adequado': 'adequate',
        'moderado': 'moderate',
        'baixo': 'low',
        'crítico': 'critical',
        'critico': 'critical'
    };
    const ordemTipos = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'];
    ordemTipos.forEach(tipo => {
        if (estoque[tipo]) {
            const info = estoque[tipo];
            // Ensure we compute status from unidades (bolsas) using authoritative thresholds
            // <=59 -> crítico, 60-99 -> baixo, 100-149 -> moderado, >=150 -> adequado
            const unidades = Number(info.unidades) || 0;
            let statusKey = 'adequado';
            if (unidades <= 59) statusKey = 'critico';
            else if (unidades <= 99) statusKey = 'baixo';
            else if (unidades <= 149) statusKey = 'moderado';
            else statusKey = 'adequado';

            // Map Portuguese statusKey to CSS class used by frontend
            const status = statusMap[statusKey] || 'adequate';
            const percent = info.percent || 0;
            // Display label based on computed statusKey (capitalized Portuguese)
            const statusLabelMap = {
                'critico': 'CRÍTICO',
                'baixo': 'BAIXO',
                'moderado': 'MODERADO',
                'adequado': 'ADEQUADO'
            };
            const statusLabel = statusLabelMap[statusKey] || (info.status || 'ADEQUADO');
            html += `
            <div class="blood-stock-card ${status}">
                <div class="blood-info">
                    <i class="fas fa-tint"></i>
                    <span class="blood-type">${tipo}</span>
                </div>
                <div class="blood-progress">
                    <div class="progress">
                        <div class="progress-bar ${status}" style="width: ${percent}%"></div>
                    </div>
                    <span class="units">${info.unidades} unidades</span>
                </div>
                <span class="status">${statusLabel}</span>
            </div>
            `;
        }
    });
    estoqueEl.innerHTML = html;
    // Reaplica evento de compatibilidade
    estoqueEl.querySelectorAll('.blood-stock-card').forEach(function (card) {
        card.addEventListener('click', function () {
            const tipo = card.querySelector('.blood-type')?.textContent?.trim();
            if (tipo) mostrarCompatibilidade(tipo);
        });
    });
}

// Função para normalizar as chaves do estoque
function normalizarEstoque(estoque) {
    const mapTipos = {
        "Anegativo": "A-",
        "Apositivo": "A+",
        "Bnegativo": "B-",
        "Bpositivo": "B+",
        "ABnegativo": "AB-",
        "ABpositivo": "AB+",
        "Onegativo": "O-",
        "Opositivo": "O+"
    };
    const estoqueNormalizado = {};
    for (const key in estoque) {
        // Se a chave já está no formato correto (A+, A-, etc.)
        let tipoNormalizado = key;

        // Se a chave está no formato antigo (Apositivo, etc.), mapear para o novo
        if (mapTipos[key]) {
            tipoNormalizado = mapTipos[key];
        }

        estoqueNormalizado[tipoNormalizado] = {
            unidades: estoque[key].quantidade,
            // Normalize status to a lowercase Portuguese term for consistent mapping
            status: (estoque[key].status || '').toString(),
            // Server returns 'porcentagem' as fraction (0..1). Convert to 0..100
            percent: Math.round((estoque[key].porcentagem || 0) * 100)
        };
    }
    return estoqueNormalizado;
}

// Adiciona evento de clique para todos os cards de sangue
document.querySelectorAll('.blood-stock-card').forEach(function (card) {
    card.addEventListener('click', function () {
        const tipo = card.querySelector('.blood-type')?.textContent?.trim();
        if (tipo) mostrarCompatibilidade(tipo);
    });
});
