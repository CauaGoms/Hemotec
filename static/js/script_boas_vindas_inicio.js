// Garante que o script só execute após o carregamento completo do HTML.
document.addEventListener("DOMContentLoaded", async function () {

  console.log("Iniciando a configuração do mapa...");

  // 1. INICIALIZAÇÃO DO MAPA
  // Cria o mapa e define uma visão inicial.
  const mapa = L.map("mapa").setView([-20.839, -41.112], 12);

  // Adiciona a camada visual do mapa (os "azulejos") do OpenStreetMap.
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors"
  }).addTo(mapa);

  let iconeGota, iconeUsuario;

  // 2. BUSCA E EXIBIÇÃO DAS UNIDADES DE COLETA E CÁLCULO DE ROTA
  let unidades = [];
  let unidadesArray = [];
  try {
    const response = await fetch("/api/unidades");
    if (!response.ok) {
      throw new Error(`A resposta da API não foi bem-sucedida: ${response.statusText}`);
    }
    unidades = await response.json();
    console.log("sucesso: Dados das unidades recebidos da API:", unidades);

    iconeGota = L.icon({
      iconUrl: "/static/img/gota.png",
      iconSize: [40, 40],
      iconAnchor: [20, 40],
      popupAnchor: [0, -35]
    });
    iconeUsuario = L.icon({
      iconUrl: "/static/img/gota.png",
      iconSize: [50, 50],
      iconAnchor: [25, 50],
      popupAnchor: [0, -45]
    });

    // Adiciona marcadores das unidades
    if (unidades && unidades.length > 0) {
      unidades.forEach(function (unidadeObjeto) {
        const nome = Object.keys(unidadeObjeto)[0];
        const coords = unidadeObjeto[nome];
        if (nome && coords && coords.length === 2) {
          const marker = L.marker(coords, { icon: iconeGota }).addTo(mapa)
            .bindPopup(`<strong>${nome}</strong>`);
          unidadesArray.push({ nome, coords, marker }); // Armazena o marcador
        }
      });
    } else {
      console.warn("Aviso: Nenhuma unidade de coleta foi retornada pela API.");
    }

  } catch (error) {
    console.error("ERRO CRÍTICO: Falha ao buscar ou processar os dados das unidades.", error);
    
    // Fallback: usar dados simulados para desenvolvimento/teste
    unidades = [
      {"Hospital Evangélico":[-20.843485026484874,-41.113190979813844]},
      {"Santa Casa":[-20.85124724515817,-41.11350464599875]}
    ];
    console.log("Usando dados de unidades simulados devido a erro na API.");
    
    // Definir ícones para fallback
    iconeGota = L.icon({
      iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png",
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",
      shadowSize: [41, 41]
    });
    iconeUsuario = L.icon({
      iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png",
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",
      shadowSize: [41, 41]
    });
    
    // Adicionar marcadores para dados simulados
    unidades.forEach(function (unidadeObjeto) {
      const nome = Object.keys(unidadeObjeto)[0];
      const coords = unidadeObjeto[nome];
      if (nome && coords && coords.length === 2) {
        const marker = L.marker(coords, { icon: iconeGota }).addTo(mapa)
          .bindPopup(`<strong>${nome}</strong>`);
        unidadesArray.push({ nome, coords, marker });
      }
    });
  }

  // 3. GERENCIAMENTO DA LOCALIZAÇÃO DO USUÁRIO E CÁLCULO DE ROTA
  console.log("Solicitando localização do usuário...");
  
  mapa.on("locationfound", function (e) {
    console.log("Sucesso: Localização do usuário encontrada!", e.latlng);
    const userMarker = L.marker(e.latlng, { icon: iconeUsuario }).addTo(mapa)
      .bindPopup("<strong>Você está aqui</strong>");
    userMarker.openPopup(); // Abre o popup do usuário

    // Encontrar unidade mais próxima
    let unidadeProxima = null;
    let menorDistancia = Infinity;
    unidadesArray.forEach(unidade => {
      const dist = mapa.distance(e.latlng, unidade.coords);
      if (dist < menorDistancia) {
        menorDistancia = dist;
        unidadeProxima = unidade;
      }
    });

    if (unidadeProxima) {
      // Traçar rota
      L.Routing.control({
        waypoints: [
          L.latLng(e.latlng.lat, e.latlng.lng),
          L.latLng(unidadeProxima.coords[0], unidadeProxima.coords[1])
        ],
        routeWhileDragging: false,
        show: false,
        addWaypoints: false,
        draggableWaypoints: false,
        createMarker: function () { return null; }
      }).on("routesfound", function (ev) {
        const route = ev.routes[0];
        const distanciaKm = (route.summary.totalDistance / 1000).toFixed(2);
        const tempoMin = Math.round(route.summary.totalTime / 60);
        
        // Exibe informações na tela
        let infoDiv = document.getElementById("info-rota");
        if (!infoDiv) {
          infoDiv = document.createElement("div");
          infoDiv.id = "info-rota";
          infoDiv.className = "alert alert-info mt-3";
          document.querySelector(".map-container").appendChild(infoDiv);
        }
        infoDiv.innerHTML = `
          <b>Unidade mais próxima:</b> ${unidadeProxima.nome}<br>
          <b>Distância:</b> ${distanciaKm} km<br>
          <b>Tempo estimado:</b> ${tempoMin} min
        `;

        // Foca o mapa na rota completa
        mapa.fitBounds(route.coordinates);

      }).addTo(mapa);
    }
  });

  // Evento acionado se houver erro ao obter a localização
  mapa.on("locationerror", function (e) {
    console.error("Erro ao obter localização:", e.message);
    alert("Não foi possível obter sua localização. Verifique se você permitiu o acesso à localização no navegador.");
  });

  // Inicia o processo para encontrar a localização do usuário.
  mapa.locate({ setView: false, maxZoom: 16 });

});

