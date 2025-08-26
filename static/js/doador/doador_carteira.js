document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("download-btn");
  const card = document.getElementById("donor-card");
  const MARGIN_MM = 10;

  if (!btn || !card) {
    alert("Não foi possível encontrar a carteirinha ou o botão de download na página.");
    return;
  }

  function getJsPDF() {
    if (window.jspdf && window.jspdf.jsPDF) return window.jspdf.jsPDF;
    if (window.jsPDF) return window.jsPDF;
    throw new Error("jsPDF não encontrado. Verifique se a biblioteca foi carregada corretamente.");
  }

  const pxToMm = (px) => px * 0.2645833333;
  const mmToPx = (mm) => Math.round(mm / 0.2645833333);

  function withDisabled(el, htmlWhile) {
    const original = el.innerHTML;
    el.disabled = true;
    if (htmlWhile) el.innerHTML = htmlWhile;
    return () => {
      el.disabled = false;
      el.innerHTML = original;
    };
  }

  async function generatePDF() {
    const restoreBtn = withDisabled(
      btn,
      '<i class="fas fa-spinner fa-spin me-2"></i>Gerando PDF...'
    );
    try {
      const jsPDF = getJsPDF();
      const doc = new jsPDF({
        orientation: "landscape",
        unit: "mm",
        format: "a4",
        compress: true,
      });

      const pageW = doc.internal.pageSize.getWidth();
      const pageH = doc.internal.pageSize.getHeight();
      const maxW = pageW - MARGIN_MM * 2;
      const maxH = pageH - MARGIN_MM * 2;

      const targetWidthPx = Math.max(mmToPx(maxW), 1400);

      const SCALE = 3;
      const canvas = await html2canvas(card, {
        scale: SCALE,
        backgroundColor: "#ffffff",
        useCORS: true,
        allowTaint: true, // Permitir taint para tentar capturar tudo, mas pode causar problemas de segurança
        ignoreElements: (element) => {
          // Ignorar elementos que podem causar problemas de CORS ou taint
          // Por exemplo, se o QR Code for de um domínio diferente e não tiver CORS configurado corretamente
          return (
            element.tagName === "IMG" &&
            element.src.includes("api.qrserver.com")
          );
        },
        onclone: (document) => {
          // Remover o QR Code do DOM clonado antes de renderizar
          const qrCodeElement = document.querySelector(".qr-code img");
          if (qrCodeElement) {
            qrCodeElement.remove();
          }
        },
      });

      const imgData = canvas.toDataURL("image/jpeg", 0.98);

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

      doc.addImage(imgData, "JPEG", x, y, renderW, renderH, undefined, "FAST");
      doc.save("carteira-doador-hemotec.pdf");
    } catch (err) {
      console.error("Erro ao gerar PDF:", err);
      alert(
        "Erro ao gerar PDF. Verifique o console para mais detalhes e se jsPDF e html2canvas foram carregados."
      );
    } finally {
      restoreBtn();
    }
  }

  btn.addEventListener("click", generatePDF);
});