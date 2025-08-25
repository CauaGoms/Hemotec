// Garante que o script só execute após o carregamento completo do HTML.
document.addEventListener("DOMContentLoaded", async function () {

  console.log("Iniciando a configuração do mapa...");

  const mapa = L.map("mapa").setView([-20.839, -41.112], 12);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors"
  }).addTo(mapa);

  let iconeGota, iconeUsuario;
  let unidades = [];
  let unidadesArray = [];

  try {
    const response = await fetch("/api/unidades");
    if (!response.ok) throw new Error(`A resposta da API não foi bem-sucedida: ${response.statusText}`);
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

    if (unidades && unidades.length > 0) {
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

  } catch (error) {
    console.error("ERRO CRÍTICO: Falha ao buscar ou processar os dados das unidades.", error);
    unidades = [
      {"Hospital Evangélico":[-20.843485026484874,-41.113190979813844]},
      {"Santa Casa":[-20.85124724515817,-41.11350464599875]}
    ];
    console.log("Usando dados de unidades simulados devido a erro na API.");

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

  async function atualizarEstoque(codUnidade, nomeUnidade) {
    try {
      console.log(`Buscando estoque da unidade ${codUnidade} (${nomeUnidade})`);

      const response = await fetch(`/api/estoque/${codUnidade}`);
      if (!response.ok) throw new Error(`Erro ao buscar estoque: ${response.statusText}`);

      const data = await response.json();
      console.log("Dados do estoque recebidos:", data);

      if (data.success && data.estoque) {
        // Atualiza o nome da unidade no título
        const spanNomeUnidade = document.getElementById("nome-unidade-estoque");
        if (spanNomeUnidade) {
          spanNomeUnidade.textContent = `${nomeUnidade} (Unidade mais próxima)`;
        }

        const tiposSanguineos = ["O+", "A+", "B+", "AB+", "O-", "A-", "B-", "AB-"];
        tiposSanguineos.forEach(tipo => {
          const estoqueItem = data.estoque[tipo];
          if (estoqueItem) {
            atualizarItemEstoque(tipo, estoqueItem);
          } else {
            atualizarItemEstoque(tipo, { status: "Crítico", classe: "bg-danger", porcentagem: 0, quantidade: 0 });
          }
        });

        atualizarMensagemAlerta(data.estoque);
      }

    } catch (error) {
      console.error("Erro ao buscar estoque:", error);
    }
  }

  function atualizarItemEstoque(tipo, dados) {
    const elementos = document.querySelectorAll(".fw-bold");
    let elementoTipo = null;
    elementos.forEach(el => {
      if (el.textContent.trim() === tipo) elementoTipo = el;
    });
    if (elementoTipo) {
      const container = elementoTipo.closest(".mb-3");
      if (container) {
        const badge = container.querySelector(".badge");
        if (badge) {
          badge.textContent = dados.status;
          badge.className = `badge ${dados.classe}`;
        }
        const progressBar = container.querySelector(".progress-bar");
        if (progressBar) {
          progressBar.style.width = `${dados.porcentagem}%`;
          progressBar.className = `progress-bar ${dados.classe}`;
          progressBar.setAttribute("aria-valuenow", dados.porcentagem);
        }
      }
    }
  }

  function atualizarMensagemAlerta(estoque) {
    const alertElement = document.querySelector(".alert.alert-danger");
    if (alertElement) {
      const tiposCriticos = [];
      Object.keys(estoque).forEach(tipo => {
        if (estoque[tipo].status === "Crítico") tiposCriticos.push(tipo);
      });
      if (tiposCriticos.length > 0) {
        alertElement.innerHTML = `<small><i class="fas fa-heart me-1"></i>Sua doação pode salvar vidas! Tipos ${tiposCriticos.join(", ")} são urgentes.</small>`;
      } else {
        alertElement.innerHTML = `<small><i class="fas fa-heart me-1"></i>Obrigado por considerar a doação de sangue!</small>`;
      }
    }
  }

  mapa.on("locationfound", function (e) {
    console.log("Sucesso: Localização do usuário encontrada!", e.latlng);
    const userMarker = L.marker(e.latlng, { icon: iconeUsuario }).addTo(mapa)
      .bindPopup("<strong>Você está aqui</strong>");
    userMarker.openPopup();

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

        mapa.fitBounds(route.coordinates);
        if (unidadeProxima.marker) unidadeProxima.marker.openPopup();

        const codUnidade = obterCodigoUnidade(unidadeProxima.nome);
        if (codUnidade) {
          atualizarEstoque(codUnidade, unidadeProxima.nome);
        }
      }).addTo(mapa);
    }
  });

  function obterCodigoUnidade(nomeUnidade) {
    const mapeamento = {
      "Hospital Evangélico": 1,
      "Santa Casa": 2
    };
    return mapeamento[nomeUnidade] || 1;
  }

  mapa.on("locationerror", function (e) {
    console.error("Erro ao obter localização:", e.message);
    alert("Não foi possível obter sua localização. Verifique se você permitiu o acesso à localização no navegador.");
  });

  mapa.locate({ setView: false, maxZoom: 16 });

});
