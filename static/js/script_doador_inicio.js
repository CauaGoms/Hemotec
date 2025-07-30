function agendarDoacao( ) {
        alert('Redirecionando para o agendamento de doação...');
        // Aqui você pode redirecionar para a página de agendamento
        // window.location.href = 'agendamento.html';
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
        handleScrollAnimations();
        handleNavbarScroll();
    });

    // E também é chamado ao carregar a página:
    document.addEventListener('DOMContentLoaded', () => {
        // ...
        handleNavbarScroll();
    });