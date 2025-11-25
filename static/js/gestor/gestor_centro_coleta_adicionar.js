// Adicionar Centro de Coleta - JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formAdicionarCentro');
    const cepInput = document.getElementById('cep');
    const telefoneInput = document.getElementById('telefone');

    // Máscara de CEP
    if (cepInput) {
        cepInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 8) value = value.slice(0, 8);
            if (value.length > 5) {
                value = value.slice(0, 5) + '-' + value.slice(5);
            }
            e.target.value = value;
        });

        cepInput.addEventListener('blur', function() {
            const cep = this.value.replace(/\D/g, '');
            if (cep.length === 8) {
                lookupCEP(cep);
            }
        });
    }

    // Máscara de telefone
    if (telefoneInput) {
        telefoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 11) value = value.slice(0, 11);
            if (value.length > 6) {
                value = '(' + value.slice(0, 2) + ') ' + value.slice(2, 7) + '-' + value.slice(7);
            } else if (value.length > 2) {
                value = '(' + value.slice(0, 2) + ') ' + value.slice(2);
            }
            e.target.value = value;
        });
    }

    // Buscar CEP
    async function lookupCEP(cep) {
        try {
            const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
            const data = await response.json();
            
            if (!data.erro) {
                document.getElementById('logradouro').value = data.logradouro || '';
                document.getElementById('bairro').value = data.bairro || '';
                
                if (data.localidade) {
                    await buscarCidade(data.localidade, data.uf);
                }
            }
        } catch (error) {
            console.error('Erro ao buscar CEP:', error);
        }
    }

    // Buscar cidade
    async function buscarCidade(nomeCidade, uf) {
        try {
            const response = await fetch('/api/cidades');
            const cidades = await response.json();
            
            const cidadeEncontrada = cidades.find(c => 
                c.nome_cidade.toLowerCase() === nomeCidade.toLowerCase() && 
                c.sigla_estado === uf
            );
            
            if (cidadeEncontrada) {
                document.getElementById('cidade').value = `${cidadeEncontrada.nome_cidade} - ${cidadeEncontrada.sigla_estado}`;
                document.getElementById('cod_cidade').value = cidadeEncontrada.cod_cidade;
            }
        } catch (error) {
            console.error('Erro ao buscar cidade:', error);
        }
    }

    // Submit form
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();

            const formData = {
                nome: document.getElementById('nome').value,
                telefone: document.getElementById('telefone').value,
                email: document.getElementById('email').value,
                cep: document.getElementById('cep').value,
                logradouro: document.getElementById('logradouro').value,
                numero: document.getElementById('numero').value || '',
                bairro: document.getElementById('bairro').value,
                cod_cidade: document.getElementById('cod_cidade').value,
                complemento: document.getElementById('complemento').value || ''
            };

            try {
                const response = await fetch('/api/gestor/centro-coleta/adicionar', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });

                const result = await response.json();

                if (response.ok) {
                    alert('Centro de coleta adicionado com sucesso!');
                    window.location.href = '/gestor/centro-coleta';
                } else {
                    alert('Erro: ' + result.message);
                }
            } catch (error) {
                console.error('Erro:', error);
                alert('Erro ao adicionar centro de coleta');
            }
        });
    }
});
