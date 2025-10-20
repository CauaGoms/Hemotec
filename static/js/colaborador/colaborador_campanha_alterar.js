// Alterar Campanha - JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const form = document.getElementById('campaignForm');
    const fileInput = document.getElementById('foto');
    const fileUploadArea = document.getElementById('fileUploadArea');
    const uploadPlaceholder = document.getElementById('uploadPlaceholder');
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const removeImageBtn = document.getElementById('removeImage');
    const previewBtn = document.getElementById('previewBtn');
    const submitBtn = document.getElementById('submitBtn');
    
    // Elementos do modal de preview
    const previewModal = new bootstrap.Modal(document.getElementById('previewModal'));
    const successModal = new bootstrap.Modal(document.getElementById('successModal'));
    
    // Variáveis de estado
    let selectedFile = null;
    let formData = {};
    
    // Inicialização
    init();
    
    function init() {
        setupEventListeners();
        setupFormValidation();
        setupDateValidation();
        loadCurrentData();
    }
    
    // Carregar dados atuais da campanha
    function loadCurrentData() {
        const codCampanha = document.getElementById('cod_campanha').value;
        if (!codCampanha) return;
        
        // Os dados já estão pré-preenchidos pelo template Jinja2
        // Apenas certificar que as datas estão no formato correto
        const dataInicio = document.getElementById('data_inicio');
        const dataFim = document.getElementById('data_fim');
        
        if (dataInicio.value) {
            dataInicio.value = new Date(dataInicio.value).toISOString().split('T')[0];
        }
        if (dataFim.value) {
            dataFim.value = new Date(dataFim.value).toISOString().split('T')[0];
        }
    }
    
    // Configurar Event Listeners
    function setupEventListeners() {
        // Upload de arquivo
        fileUploadArea.addEventListener('click', () => fileInput.click());
        fileUploadArea.addEventListener('dragover', handleDragOver);
        fileUploadArea.addEventListener('dragleave', handleDragLeave);
        fileUploadArea.addEventListener('drop', handleDrop);
        fileInput.addEventListener('change', handleFileSelect);
        removeImageBtn.addEventListener('click', removeImage);
        
        // Botões
        previewBtn.addEventListener('click', showPreview);
        form.addEventListener('submit', handleSubmit);
        
        // Validação em tempo real
        const inputs = form.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', validateField);
            input.addEventListener('input', clearValidation);
        });
    }
    
    // Configurar validação de formulário
    function setupFormValidation() {
        // Contador de caracteres para textarea
        const descricaoTextarea = document.getElementById('descricao');
        const tituloInput = document.getElementById('titulo');
        
        if (descricaoTextarea) {
            descricaoTextarea.addEventListener('input', function() {
                updateCharacterCount(this, 1000);
            });
        }
        
        if (tituloInput) {
            tituloInput.addEventListener('input', function() {
                updateCharacterCount(this, 100);
            });
        }
    }
    
    // Configurar validação de datas
    function setupDateValidation() {
        const dataInicio = document.getElementById('data_inicio');
        const dataFim = document.getElementById('data_fim');
        
        // Definir data mínima como hoje
        const today = new Date().toISOString().split('T')[0];
        dataInicio.min = today;
        dataFim.min = today;
        
        dataInicio.addEventListener('change', function() {
            dataFim.min = this.value;
            if (dataFim.value && dataFim.value < this.value) {
                dataFim.value = this.value;
            }
            validateDateRange();
        });
        
        dataFim.addEventListener('change', validateDateRange);
    }
    
    // Atualizar contador de caracteres
    function updateCharacterCount(element, maxLength) {
        const currentLength = element.value.length;
        const feedback = element.parentNode.querySelector('.form-feedback small');
        
        if (feedback) {
            feedback.textContent = `${currentLength}/${maxLength} caracteres`;
            
            if (currentLength > maxLength * 0.9) {
                feedback.style.color = '#ffc107';
            } else if (currentLength === maxLength) {
                feedback.style.color = '#dc3545';
            } else {
                feedback.style.color = '#6c757d';
            }
        }
    }
    
    // Validar campo individual
    function validateField(event) {
        const field = event.target;
        const value = field.value.trim();
        let isValid = true;
        let message = '';
        
        // Limpar validação anterior
        clearFieldValidation(field);
        
        // Validações específicas por campo
        switch (field.id) {
            case 'titulo':
                if (!value) {
                    isValid = false;
                    message = 'Título é obrigatório';
                } else if (value.length < 5) {
                    isValid = false;
                    message = 'Título deve ter pelo menos 5 caracteres';
                } else if (value.length > 100) {
                    isValid = false;
                    message = 'Título não pode exceder 100 caracteres';
                }
                break;
                
            case 'descricao':
                if (!value) {
                    isValid = false;
                    message = 'Descrição é obrigatória';
                } else if (value.length < 20) {
                    isValid = false;
                    message = 'Descrição deve ter pelo menos 20 caracteres';
                } else if (value.length > 1000) {
                    isValid = false;
                    message = 'Descrição não pode exceder 1000 caracteres';
                }
                break;
                
            case 'data_inicio':
                if (!value) {
                    isValid = false;
                    message = 'Data de início é obrigatória';
                }
                break;
                
            case 'data_fim':
                if (!value) {
                    isValid = false;
                    message = 'Data de término é obrigatória';
                } else {
                    const dataInicio = document.getElementById('data_inicio').value;
                    if (dataInicio && new Date(value) < new Date(dataInicio)) {
                        isValid = false;
                        message = 'Data de término deve ser posterior à data de início';
                    }
                }
                break;
        }
        
        // Aplicar validação visual
        if (isValid) {
            field.classList.add('is-valid');
            field.classList.remove('is-invalid');
        } else {
            field.classList.add('is-invalid');
            field.classList.remove('is-valid');
            showFieldError(field, message);
        }
        
        return isValid;
    }
    
    // Limpar validação de campo
    function clearValidation(event) {
        const field = event.target;
        clearFieldValidation(field);
    }
    
    function clearFieldValidation(field) {
        field.classList.remove('is-valid', 'is-invalid');
        const existingFeedback = field.parentNode.querySelector('.invalid-feedback, .valid-feedback');
        if (existingFeedback) {
            existingFeedback.remove();
        }
    }
    
    // Mostrar erro de campo
    function showFieldError(field, message) {
        const feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        feedback.textContent = message;
        field.parentNode.appendChild(feedback);
    }
    
    // Validar intervalo de datas
    function validateDateRange() {
        const dataInicio = document.getElementById('data_inicio');
        const dataFim = document.getElementById('data_fim');
        
        if (dataInicio.value && dataFim.value) {
            const inicio = new Date(dataInicio.value);
            const fim = new Date(dataFim.value);
            
            if (fim < inicio) {
                dataFim.classList.add('is-invalid');
                showFieldError(dataFim, 'Data de término deve ser posterior à data de início');
                return false;
            } else {
                clearFieldValidation(dataFim);
                dataFim.classList.add('is-valid');
                return true;
            }
        }
        return true;
    }
    
    // Manipulação de arquivos
    function handleDragOver(event) {
        event.preventDefault();
        fileUploadArea.classList.add('dragover');
    }
    
    function handleDragLeave(event) {
        event.preventDefault();
        fileUploadArea.classList.remove('dragover');
    }
    
    function handleDrop(event) {
        event.preventDefault();
        fileUploadArea.classList.remove('dragover');
        
        const files = event.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    }
    
    function handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            handleFile(file);
        }
    }
    
    function handleFile(file) {
        // Validar tipo de arquivo
        if (!file.type.startsWith('image/')) {
            showAlert('Erro', 'Por favor, selecione apenas arquivos de imagem.', 'error');
            return;
        }
        
        // Validar tamanho do arquivo (5MB)
        if (file.size > 5 * 1024 * 1024) {
            showAlert('Erro', 'O arquivo deve ter no máximo 5MB.', 'error');
            return;
        }
        
        selectedFile = file;
        displayImagePreview(file);
    }
    
    function displayImagePreview(file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImg.src = e.target.result;
            uploadPlaceholder.style.display = 'none';
            imagePreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
    
    function removeImage() {
        selectedFile = null;
        fileInput.value = '';
        previewImg.src = '';
        uploadPlaceholder.style.display = 'block';
        imagePreview.style.display = 'none';
    }
    
    // Mostrar preview da campanha
    function showPreview() {
        if (!validateForm()) {
            showAlert('Atenção', 'Por favor, corrija os erros no formulário antes de visualizar.', 'warning');
            return;
        }
        
        // Coletar dados do formulário
        formData = {
            titulo: document.getElementById('titulo').value,
            descricao: document.getElementById('descricao').value,
            data_inicio: document.getElementById('data_inicio').value,
            data_fim: document.getElementById('data_fim').value,
            foto: selectedFile
        };
        
        // Atualizar modal de preview
        updatePreviewModal();
        previewModal.show();
    }
    
    function updatePreviewModal() {
        document.getElementById('previewTitulo').textContent = formData.titulo;
        document.getElementById('previewDescricao').textContent = formData.descricao;
        
        // Formatar datas
        const dataInicio = new Date(formData.data_inicio).toLocaleDateString('pt-BR');
        const dataFim = new Date(formData.data_fim).toLocaleDateString('pt-BR');
        
        document.getElementById('previewDataInicio').textContent = dataInicio;
        document.getElementById('previewDataFim').textContent = dataFim;
        
        // Mostrar imagem se houver
        const previewImageContainer = document.getElementById('previewImagem');
        if (formData.foto) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImageContainer.innerHTML = `<img src="${e.target.result}" alt="Preview da campanha" style="width: 100%; max-height: 250px; object-fit: cover; border-radius: 12px;">`;
            };
            reader.readAsDataURL(formData.foto);
        } else {
            previewImageContainer.innerHTML = '<div class="text-muted p-4" style="background: #f8f9fa; border-radius: 12px;"><i class="fas fa-image fa-2x mb-2"></i><br>Nenhuma imagem nova selecionada</div>';
        }
    }
    
    // Validar formulário completo
    function validateForm() {
        const requiredFields = ['titulo', 'descricao', 'data_inicio', 'data_fim'];
        let isValid = true;
        
        requiredFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            const fieldValid = validateField({ target: field });
            if (!fieldValid) {
                isValid = false;
            }
        });
        
        return isValid && validateDateRange();
    }
    
    // Submeter formulário
    function handleSubmit(event) {
        event.preventDefault();
        
        if (!validateForm()) {
            showAlert('Erro', 'Por favor, corrija os erros no formulário.', 'error');
            return;
        }
        
        // Mostrar loading
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;
        
        const codCampanha = document.getElementById('cod_campanha').value;
        
        // Preparar FormData
        const formDataObj = new FormData();
        formDataObj.append('titulo', document.getElementById('titulo').value);
        formDataObj.append('descricao', document.getElementById('descricao').value);
        formDataObj.append('data_inicio', document.getElementById('data_inicio').value);
        formDataObj.append('data_fim', document.getElementById('data_fim').value);
        if (selectedFile) {
            formDataObj.append('foto', selectedFile);
        }
        
        // Fazer POST para o servidor
        fetch(`/api/colaborador/campanha/editar/${codCampanha}`, {
            method: 'POST',
            body: formDataObj
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
            
            if (data.success) {
                // Mostrar modal de sucesso
                successModal.show();
                
                // Redirecionar após sucesso
                setTimeout(() => {
                    window.location.href = '/colaborador/campanha';
                }, 2000);
            } else {
                showAlert('Erro', data.message || 'Erro ao atualizar campanha', 'error');
            }
        })
        .catch(error => {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
            showAlert('Erro', error.message || 'Erro ao atualizar campanha', 'error');
        });
    }
    
    // Resetar formulário
    function resetForm() {
        form.reset();
        removeImage();
        
        // Limpar validações
        const fields = form.querySelectorAll('.form-control');
        fields.forEach(field => {
            clearFieldValidation(field);
        });
    }
    
    // Mostrar alerta
    function showAlert(title, message, type = 'info') {
        // Criar modal de alerta dinâmico
        const alertModal = document.createElement('div');
        alertModal.className = 'modal fade';
        alertModal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header bg-${type === 'error' ? 'danger' : type === 'warning' ? 'warning' : 'info'} text-white">
                        <h5 class="modal-title">
                            <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : type === 'warning' ? 'exclamation-circle' : 'info-circle'}"></i>
                            ${title}
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>${message}</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(alertModal);
        const modal = new bootstrap.Modal(alertModal);
        modal.show();
        
        // Remover modal após fechar
        alertModal.addEventListener('hidden.bs.modal', () => {
            document.body.removeChild(alertModal);
        });
    }
});
