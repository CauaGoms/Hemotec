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

function verCampanhas() {
    window.location.href = '/doador/campanha';
}

function novoDoador() {
    window.location.href = '/doador/novo_doador';
}

function verEstoque() {
    alert('Redirecionando para visualização do estoque...');
    // window.location.href = 'estoque.html';
}

function gerarRelatorio() {
    alert('Redirecionando para geração de relatórios...');
    // window.location.href = 'relatorios.html';
}

// Atualizar dados em tempo real (simulação)
function atualizarDados() {
    // Aqui você pode implementar chamadas AJAX para atualizar os dados
    console.log('Atualizando dados do dashboard...');
}

// Atualizar dados a cada 5 minutos
setInterval(atualizarDados, 300000);

function handleNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
        navbar.style.backdropFilter = 'blur(10px)';
    } else {
        navbar.style.backgroundColor = 'white';
        navbar.style.backdropFilter = 'none';
    }
}

window.addEventListener('scroll', () => {
    // handleScrollAnimations(); // Comentado para evitar erro
    handleNavbarScroll();
});

// E também é chamado ao carregar a página:
document.addEventListener('DOMContentLoaded', () => {
    console.log('JS doador_inicio carregado!');
    handleNavbarScroll();
    // Adiciona evento de clique para todos os cards de sangue
    document.querySelectorAll('.blood-stock-card').forEach(function(card) {
        card.addEventListener('click', function() {
            const tipo = card.querySelector('.blood-type')?.textContent?.trim();
            console.log('Card clicado:', tipo);
            if (tipo) mostrarCompatibilidade(tipo);
        });
    });
});