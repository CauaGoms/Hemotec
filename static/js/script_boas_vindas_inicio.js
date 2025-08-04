// Bloco de código seguro para inicializar o mapa e os marcadores
document.addEventListener('DOMContentLoaded', function () {

  // 1. Inicializa a variável 'unidades' de forma segura
  // O Jinja2 irá substituir esta seção pelo array de coordenadas ou por 'null'
  // {% include "partials/coordenada_var.jinja" %}

  // 2. Inicializa o mapa
  const mapa = L.map('mapa').setView([-20.839, -41.112], 12);

  // 3. Adiciona a camada de fundo (tile layer) do OpenStreetMap
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(mapa);

  // 4. Define o ícone personalizado para as unidades de coleta
  const iconeGota = L.icon({
    iconUrl: '/static/img/gota.png', // IMPORTANTE: Verifique se este caminho está correto
    iconSize: [40, 40],
    iconAnchor: [20, 40],
    popupAnchor: [0, -35]
  });

  // 5. Adiciona os marcadores das unidades se a variável 'unidades' existir
  if (unidades && unidades.length > 0) {
    unidades.forEach(function (unidade) {
      const nome = Object.keys(unidade)[0];
      const coords = unidade[nome];
      L.marker(coords, { icon: iconeGota }).addTo(mapa)
        .bindPopup(`<strong>${nome}</strong>`);
    });
  } else {
    console.warn("Nenhuma coordenada de unidade de coleta foi fornecida pelo backend.");
  }

  // 6. Gerencia a localização do usuário
  mapa.on('locationfound', function (e) {
    console.log("Localização do usuário encontrada:", e.latlng);
    // Usa o marcador padrão do Leaflet (azul) para a localização do usuário
    L.marker(e.latlng).addTo(mapa)
      .bindPopup("<strong>Você está aqui</strong>").openPopup();
  });

  mapa.on('locationerror', function (e) {
    console.error("Erro ao obter localização:", e.message);
    // Opcional: Informar o usuário de forma não intrusiva
    // alert("Não foi possível obter sua localização. Verifique as permissões no seu navegador.");
  });

  // Inicia o processo de geolocalização
  mapa.locate({ setView: true, maxZoom: 14 });

});