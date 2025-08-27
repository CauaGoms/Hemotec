document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const confirmarExclusaoBtn = document.getElementById('confirmarExclusao');
    const excluirDefinitivoBtn = document.getElementById('excluirDefinitivo');
    const motivoRadios = document.querySelectorAll('input[name="motivo"]');
    const outrosMotivoDiv = document.querySelector('.outros-motivo');
    const outroMotivoTextarea = document.getElementById('outroMotivo');
    
    // Modais
    const confirmacaoFinalModal = new bootstrap.Modal(document.getElementById('confirmacaoFinalModal'));
    const sucessoModal = new bootstrap.Modal(document.getElementById('sucessoModal'));

    // Função para mostrar/ocultar campo "Outros"
    function toggleOutrosMotivo() {
        const outrosSelected = document.getElementById('motivo4').checked;
        if (outrosSelected) {
            outrosMotivoDiv.style.display = 'block';
            outroMotivoTextarea.focus();
        } else {
            outrosMotivoDiv.style.display = 'none';
            outroMotivoTextarea.value = '';
        }
    }

    // Event listeners para os radio buttons de motivo
    motivoRadios.forEach(radio => {
        radio.addEventListener('change', toggleOutrosMotivo);
    });

    // Função para validar o formulário
    function validarFormulario() {
        const motivoSelecionado = document.querySelector('input[name="motivo"]:checked');
        
        if (motivoSelecionado && motivoSelecionado.value === 'outros') {
            const outroMotivo = outroMotivoTextarea.value.trim();
            if (!outroMotivo) {
                mostrarAlerta('Por favor, descreva o motivo da exclusão.', 'warning');
                outroMotivoTextarea.focus();
                return false;
            }
        }
        
        return true;
    }

    // Função para mostrar alertas
    function mostrarAlerta(mensagem, tipo = 'info') {
        // Remove alertas existentes
        const alertasExistentes = document.querySelectorAll('.alert-dinamico');
        alertasExistentes.forEach(alerta => alerta.remove());

        // Cria novo alerta
        const alerta = document.createElement('div');
        alerta.className = `alert alert-${tipo} alert-dismissible fade show alert-dinamico`;
        alerta.innerHTML = `
            ${mensagem}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;

        // Insere o alerta no topo do container
        const container = document.querySelector('.exclusao-container');
        container.insertBefore(alerta, container.firstChild);

        // Remove automaticamente após 5 segundos
        setTimeout(() => {
            if (alerta.parentNode) {
                alerta.remove();
            }
        }, 5000);
    }

    // Event listener para o botão "Confirmar Exclusão"
    confirmarExclusaoBtn.addEventListener('click', function() {
        if (validarFormulario()) {
            // Adiciona efeito de loading
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processando...';
            this.disabled = true;

            // Simula processamento
            setTimeout(() => {
                this.innerHTML = originalText;
                this.disabled = false;
                confirmacaoFinalModal.show();
            }, 1000);
        }
    });

    // Event listener para o botão "Excluir Definitivo"
    excluirDefinitivoBtn.addEventListener('click', function() {
        // Adiciona efeito de loading
        const originalText = this.innerHTML;
        this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Excluindo...';
        this.disabled = true;

        // Simula exclusão no servidor
        setTimeout(() => {
            confirmacaoFinalModal.hide();
            
            // Aguarda o modal fechar completamente antes de mostrar o sucesso
            setTimeout(() => {
                sucessoModal.show();
            }, 300);
        }, 2000);
    });

    // Função para coletar dados do formulário
    function coletarDadosFormulario() {
        const motivoSelecionado = document.querySelector('input[name="motivo"]:checked');
        let motivo = null;
        let descricaoMotivo = null;

        if (motivoSelecionado) {
            motivo = motivoSelecionado.value;
            if (motivo === 'outros') {
                descricaoMotivo = outroMotivoTextarea.value.trim();
            }
        }

        return {
            agendamentoId: 'AGD-2025-001', // ID do agendamento (seria passado pelo backend)
            motivo: motivo,
            descricaoMotivo: descricaoMotivo,
            dataExclusao: new Date().toISOString()
        };
    }

    // Função para simular envio para o servidor
    function excluirAgendamento(dados) {
        return new Promise((resolve, reject) => {
            // Simula chamada AJAX
            console.log('Dados enviados para exclusão:', dados);
            
            // Simula sucesso após 2 segundos
            setTimeout(() => {
                const sucesso = Math.random() > 0.1; // 90% de chance de sucesso
                
                if (sucesso) {
                    resolve({
                        status: 'success',
                        message: 'Agendamento excluído com sucesso!'
                    });
                } else {
                    reject({
                        status: 'error',
                        message: 'Erro ao excluir agendamento. Tente novamente.'
                    });
                }
            }, 2000);
        });
    }

    // Função para animar elementos na entrada
    function animarEntrada() {
        const elementos = document.querySelectorAll('.detail-item, .warning-message, .reason-section');
        elementos.forEach((elemento, index) => {
            elemento.style.opacity = '0';
            elemento.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                elemento.style.transition = 'all 0.6s ease-out';
                elemento.style.opacity = '1';
                elemento.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }

    // Função para adicionar efeitos hover nos cards
    function adicionarEfeitosHover() {
        const detailItems = document.querySelectorAll('.detail-item');
        
        detailItems.forEach(item => {
            item.addEventListener('mouseenter', function() {
                this.style.transform = 'translateX(10px) scale(1.02)';
            });
            
            item.addEventListener('mouseleave', function() {
                this.style.transform = 'translateX(0) scale(1)';
            });
        });
    }

    // Função para salvar rascunho do motivo
    function salvarRascunho() {
        const dados = coletarDadosFormulario();
        localStorage.setItem('rascunho_exclusao', JSON.stringify(dados));
    }

    // Função para carregar rascunho do motivo
    function carregarRascunho() {
        const rascunho = localStorage.getItem('rascunho_exclusao');
        if (rascunho) {
            try {
                const dados = JSON.parse(rascunho);
                
                if (dados.motivo) {
                    const radioMotivo = document.getElementById(`motivo${getRadioIndex(dados.motivo)}`);
                    if (radioMotivo) {
                        radioMotivo.checked = true;
                        toggleOutrosMotivo();
                        
                        if (dados.motivo === 'outros' && dados.descricaoMotivo) {
                            outroMotivoTextarea.value = dados.descricaoMotivo;
                        }
                    }
                }
            } catch (e) {
                console.error('Erro ao carregar rascunho:', e);
            }
        }
    }

    // Função auxiliar para obter índice do radio button
    function getRadioIndex(valor) {
        const mapeamento = {
            'conflito_horario': '1',
            'problemas_saude': '2',
            'viagem': '3',
            'outros': '4'
        };
        return mapeamento[valor] || '1';
    }

    // Event listeners para salvar rascunho
    motivoRadios.forEach(radio => {
        radio.addEventListener('change', salvarRascunho);
    });

    outroMotivoTextarea.addEventListener('input', salvarRascunho);

    // Limpar rascunho quando a exclusão for bem-sucedida
    document.getElementById('sucessoModal').addEventListener('shown.bs.modal', function() {
        localStorage.removeItem('rascunho_exclusao');
    });

    // Função para confirmar saída da página se houver dados não salvos
    function confirmarSaida(event) {
        const dados = coletarDadosFormulario();
        if (dados.motivo || dados.descricaoMotivo) {
            event.preventDefault();
            event.returnValue = 'Você tem alterações não salvas. Deseja realmente sair?';
            return event.returnValue;
        }
    }

    // Adicionar confirmação de saída
    window.addEventListener('beforeunload', confirmarSaida);

    // Remover confirmação de saída quando navegar pelos botões da página
    document.querySelectorAll('a[href], button[type="button"]').forEach(elemento => {
        elemento.addEventListener('click', function() {
            window.removeEventListener('beforeunload', confirmarSaida);
        });
    });

    // Inicialização
    animarEntrada();
    adicionarEfeitosHover();
    carregarRascunho();

    // Adicionar tooltips nos ícones
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    console.log('Script de exclusão de agendamento carregado com sucesso!');
});