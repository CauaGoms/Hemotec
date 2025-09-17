(function(){
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

            const mapa = L.map('mapa', { zoomControl:true, attributionControl:true })
                .setView([-20.851136957150032, -41.113483188824155], 11); // Coordenadas iniciais

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
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

            function listarUnidades(){
                listaUnidades.innerHTML = '';
                unidades.forEach(u => {
                    const { cod_unidade, nome, latitude: lat, longitude: lng } = u;

                    const li = document.createElement('li');
                    li.innerHTML = '<strong>' + nome + '</strong><span>Coordenadas: ' + lat + ', ' + lng + '</span>';
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
                            .then(estoque => {
                                document.getElementById('nome-unidade-estoque').textContent = nome;
                                const estoqueEl = document.getElementById('estoque-atual');
                                if (estoqueEl) {
                                    estoqueEl.innerHTML = JSON.stringify(estoque, null, 2);
                                }
                            })
                            .catch(() => {
                                document.getElementById('nome-unidade-estoque').textContent = 'Erro ao buscar estoque';
                            });
                    });
                    li.appendChild(btn);
                    listaUnidades.appendChild(li);
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

            unidades.forEach(u => {
                const { cod_unidade, nome, latitude: lat, longitude: lng } = u;

                const m = L.marker([lat, lng], { icon: unidadeIcon }).addTo(mapa);
                m.bindPopup('<strong>' + nome + '</strong><br>Coordenadas: ' + lat + ', ' + lng + '<br><button type="button" class="btn-rota" data-id="' + cod_unidade + '">Traçar rota</button>');
                m.on('popupopen', (e) => {
                    const btn = e.popup._contentNode.querySelector('.btn-rota');
                    btn.addEventListener('click', () => {
                        if (!userMarker) {
                            statusEl.textContent = 'Obtenha sua localização primeiro.';
                            return;
                        }
                        criarRota([userMarker.getLatLng().lat, userMarker.getLatLng().lng], [lat, lng], nome);
                        // Buscar estoque da unidade selecionada
                        fetch(`/api/estoque/${cod_unidade}`)
                            .then(resp => resp.json())
                            .then(estoque => {
                                document.getElementById('nome-unidade-estoque').textContent = nome;
                                const estoqueEl = document.getElementById('estoque-atual');
                                if (estoqueEl) {
                                    estoqueEl.innerHTML = JSON.stringify(estoque, null, 2);
                                }
                            })
                            .catch(() => {
                                document.getElementById('nome-unidade-estoque').textContent = 'Erro ao buscar estoque';
                            });
                        mapa.closePopup();
                    });
                });
            });

            function obterLocalizacao() {
                if (!('geolocation' in navigator)) {
                    statusEl.textContent = 'Geolocalização não suportada.';
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
                        // Encontrar unidade mais próxima
                    let unidadeMaisProxima = null;
                    let menorDistancia = Infinity;
                    unidades.forEach(u => {
                        const { cod_unidade, nome, latitude: lat, longitude: lng } = u;
                        const dist = Math.sqrt(Math.pow(lat - latitude, 2) + Math.pow(lng - longitude, 2));
                        if (dist < menorDistancia) {
                            menorDistancia = dist;
                            unidadeMaisProxima = { cod_unidade, nome, lat, lng };
                        }
                    });
                    if (unidadeMaisProxima) {
                        // Buscar estoque da unidade mais próxima
                        fetch(`/api/estoque/${unidadeMaisProxima.cod_unidade}`)
                            .then(resp => resp.json())
                            .then(estoque => {
                                document.getElementById('nome-unidade-estoque').textContent = unidadeMaisProxima.nome;
                                // Exibir dados do estoque (exemplo)
                                const estoqueEl = document.getElementById('estoque-atual');
                                if (estoqueEl) {
                                    estoqueEl.innerHTML = JSON.stringify(estoque, null, 2);
                                }
                            })
                            .catch(() => {
                                document.getElementById('nome-unidade-estoque').textContent = 'Erro ao buscar estoque';
                            });
                    }
                }, err => {
                    statusEl.textContent = 'Erro: ' + err.message;
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

            btnLocate.addEventListener('click', obterLocalizacao);
            btnClear.addEventListener('click', () => {
                if (routingControl) {
                    mapa.removeControl(routingControl);
                    routingControl = null;
                }
                infoRota.innerHTML = '';
                btnClear.disabled = true;
            });

            listarUnidades();

            // Auto tentar localização se seguro (localhost ou https)
            if (location.protocol === 'https:' || location.hostname === 'localhost' || location.hostname === '127.0.0.1') {
                setTimeout(() => obterLocalizacao(), 600);
            } else {
                statusEl.textContent = 'Ative HTTPS ou use localhost para geolocalização automática.';
            }
        })
        .catch(error => {
            console.error('Erro ao carregar unidades:', error);
        });
})();