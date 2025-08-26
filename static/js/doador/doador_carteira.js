document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('download-btn');
  const card = document.getElementById('donor-card');

  if (!btn || !card) {
    console.error('Erro: Botão de download ou carteirinha do doador não encontrados.');
    alert('Não foi possível encontrar a carteirinha ou o botão de download na página.');
    return;
  }

  // Função para carregar dinamicamente um script
  function loadScript(url, callback) {
    const script = document.createElement('script');
    script.src = url;
    script.onload = callback;
    script.onerror = () => {
      console.error(`Erro ao carregar o script: ${url}`);
      alert(`Erro ao carregar a biblioteca necessária: ${url}`);
    };
    document.head.appendChild(script);
  }

  // Carregar jsPDF e html2canvas se ainda não estiverem disponíveis
  let jspdfLoaded = false;
  let html2canvasLoaded = false;

  if (typeof window.jspdf !== 'undefined' && typeof window.jspdf.jsPDF !== 'undefined') {
    jspdfLoaded = true;
  }
  if (typeof window.html2canvas !== 'undefined') {
    html2canvasLoaded = true;
  }

  const initPdfGeneration = () => {
    if (!jspdfLoaded || !html2canvasLoaded) return;

    const MARGIN_MM = 10;

    function getJsPDF() {
      if (window.jspdf && window.jspdf.jsPDF) return window.jspdf.jsPDF;
      if (window.jsPDF) return window.jsPDF;
      throw new Error('jsPDF não encontrado. Verifique se a biblioteca foi carregada corretamente.');
    }

    const pxToMm = px => px * 0.2645833333;
    const mmToPx = mm => Math.round(mm / 0.2645833333);

    function withDisabled(el, htmlWhile) {
      const original = el.innerHTML;
      el.disabled = true;
      if (htmlWhile) el.innerHTML = htmlWhile;
      return () => { el.disabled = false; el.innerHTML = original; };
    }

    async function generatePDF() {
      const restoreBtn = withDisabled(btn, '<i class="fas fa-spinner fa-spin me-2"></i>Gerando PDF...');
      try {
        const jsPDF = getJsPDF();
        const doc = new jsPDF({
          orientation: 'landscape',
          unit: 'mm',
          format: 'a4',
          compress: true
        });

        const pageW = doc.internal.pageSize.getWidth();
        const pageH = doc.internal.pageSize.getHeight();
        const maxW = pageW - MARGIN_MM * 2;
        const maxH = pageH - MARGIN_MM * 2;

        const targetWidthPx = Math.max(mmToPx(maxW), 1400);

        const SCALE = 3;
        const canvas = await html2canvas(card, {
          scale: SCALE,
          backgroundColor: '#ffffff',
          useCORS: true,
          allowTaint: true, // Permitir taint para tentar capturar tudo
          ignoreElements: (element) => {
            // Ignorar elementos que podem causar problemas de CORS ou taint
            // Ex: QR Code de um domínio diferente
            return (
              element.tagName === 'IMG' &&
              element.src.includes('api.qrserver.com')
            );
          },
          onclone: (clonedDoc) => {
            // Remover o QR Code do DOM clonado antes de renderizar
            const qrCodeElement = clonedDoc.querySelector('.qr-code img');
            if (qrCodeElement) {
              qrCodeElement.remove();
            }
          },
          // foreignObjectRendering: true // Pode ajudar com SVG e outros elementos complexos, mas pode ter problemas de compatibilidade
        });

        const imgData = canvas.toDataURL('image/jpeg', 0.98);

        const cssPxW = canvas.width / SCALE;
        const cssPxH = canvas.height / SCALE;
        const imgWmm = pxToMm(cssPxW);
        const imgHmm = pxToMm(cssPxH);

        let renderW = maxW;
        let renderH = (imgHmm / imgWmm) * renderW;
        if (renderH > maxH) {
          renderH = maxH;
          renderW = (imgWmm / imgHmm) * renderH;
        }

        const x = (pageW - renderW) / 2;
        const y = (pageH - renderH) / 2;

        doc.addImage(imgData, 'JPEG', x, y, renderW, renderH, undefined, 'FAST');
        doc.save('carteira-doador-hemotec.pdf');
      } catch (err) {
        console.error('Erro ao gerar PDF:', err);
        alert('Erro ao gerar PDF. Verifique o console para mais detalhes.');
      } finally {
        restoreBtn();
      }
    }

    btn.addEventListener('click', generatePDF);
  };

  // Carregar as bibliotecas se ainda não estiverem carregadas
  if (!jspdfLoaded) {
    loadScript('https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js', () => {
      jspdfLoaded = true;
      initPdfGeneration();
    });
  }

  if (!html2canvasLoaded) {
    loadScript('https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js', () => {
      html2canvasLoaded = true;
      initPdfGeneration();
    });
  }

  // Se já estiverem carregadas, inicializa imediatamente
  if (jspdfLoaded && html2canvasLoaded) {
    initPdfGeneration();
  }
});