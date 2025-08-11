// Garante que o script só execute após o carregamento completo do HTML.
document.addEventListener('DOMContentLoaded', async function () {
  
  console.log("Iniciando a configuração do mapa...");

  // 1. INICIALIZAÇÃO DO MAPA
  // Cria o mapa e define uma visão inicial.
  const mapa = L.map('mapa').setView([-20.839, -41.112], 12);

  // Adiciona a camada visual do mapa (os "azulejos") do OpenStreetMap.
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(mapa);

  let iconeGota;
  let iconeUsuario;

  // 2. BUSCA E EXIBIÇÃO DAS UNIDADES DE COLETA
  // Este bloco 'try...catch' lida com a busca de dados da sua API.
  try {
    // Faz a chamada para a API que você criou no backend.
    const response = await fetch('/api/unidades');
    
    // Se a resposta não for "OK" (ex: erro 500, 404), lança um erro.
    if (!response.ok) {
      throw new Error(`A resposta da API não foi bem-sucedida: ${response.statusText}`);
    }
    
    // Converte a resposta da API para o formato JSON.
    const unidades = await response.json();
    console.log("sucesso: Dados das unidades recebidos da API:", unidades);

    // Define o ícone personalizado para as unidades.
    iconeGota = L.icon({
      iconUrl: '/static/img/gota.png', // Verifique se o caminho está correto!
      iconSize: [40, 40],
      iconAnchor: [20, 40],
      popupAnchor: [0, -35]
    });

    iconeUsuario = L.icon({
      iconUrl: '/static/img/gota.png', // Mesmo ícone da gota
      iconSize: [50, 50], // Tamanho maior
      iconAnchor: [25, 50], // Ajuste do âncora
      popupAnchor: [0, -45]
    });

    // Itera sobre os dados recebidos para criar os marcadores.
    if (unidades && unidades.length > 0) {
      unidades.forEach(function (unidadeObjeto) {
        // Extrai o nome e as coordenadas do formato {"Nome": [lat, lon]}
        const nome = Object.keys(unidadeObjeto)[0];
        const coords = unidadeObjeto[nome];

        // Adiciona o marcador no mapa com o ícone e o pop-up.
        if (nome && coords && coords.length === 2) {
          L.marker(coords, { icon: iconeGota }).addTo(mapa)
            .bindPopup(`<strong>${nome}</strong>`);
        }
      });
    } else {
      console.warn("Aviso: Nenhuma unidade de coleta foi retornada pela API.");
    }

  } catch (error) {
    // Se qualquer parte da busca de dados falhar, exibe um erro claro.
    console.error("ERRO CRÍTICO: Falha ao buscar ou processar os dados das unidades.", error);
  }
  
  // 3. GERENCIAMENTO DA LOCALIZAÇÃO DO USUÁRIO
  console.log("Solicitando localização do usuário...");

  // Evento acionado se a localização for encontrada com sucesso.
  mapa.on('locationfound', function (e) {
    console.log("Sucesso: Localização do usuário encontrada!", e.latlng);
    L.marker(e.latlng, { icon: iconeUsuario }).addTo(mapa)
      .bindPopup("<strong>Você está aqui</strong>").openPopup();
    mapa.setView(e.latlng, 14);
  });

  // Inicia o processo para encontrar a localização do usuário.
  mapa.locate({ setView: false, maxZoom: 16 });

});