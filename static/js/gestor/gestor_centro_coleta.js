// Centro de Coleta - Lista
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const cidadeFilter = document.getElementById('cidadeFilter');
    const centroItems = document.querySelectorAll('.centro-item');

    // Função de filtro
    function filterCentros() {
        const searchTerm = searchInput.value.toLowerCase();
        const cidadeSelected = cidadeFilter.value;

        centroItems.forEach(item => {
            const title = item.getAttribute('data-title');
            const email = item.getAttribute('data-email');
            const cidade = item.getAttribute('data-cidade');

            const matchesSearch = title.includes(searchTerm) || email.includes(searchTerm);
            const matchesCidade = !cidadeSelected || cidade === cidadeSelected;

            if (matchesSearch && matchesCidade) {
                item.style.display = 'block';
                item.classList.add('fade-in');
            } else {
                item.style.display = 'none';
            }
        });
    }

    // Event listeners
    if (searchInput) {
        searchInput.addEventListener('input', filterCentros);
    }

    if (cidadeFilter) {
        cidadeFilter.addEventListener('change', filterCentros);
    }

    // Animação de entrada dos cards
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, { threshold: 0.1 });

    centroItems.forEach(item => {
        observer.observe(item);
    });
});
