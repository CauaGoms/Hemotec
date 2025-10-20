// Adicionar Campanha - JavaScript
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
                } else if (new Date(value) < new Date().setHours(0,0,0,0)) {
                    isValid = false;
                    message = 'Data de início não pode ser no passado';
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
            previewImageContainer.innerHTML = '<div class="text-muted p-4" style="background: #f8f9fa; border-radius: 12px;"><i class="fas fa-image fa-2x mb-2"></i><br>Nenhuma imagem selecionada</div>';
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
        fetch('/api/colaborador/campanha/adicionar', {
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
                
                // Limpar formulário após sucesso
                setTimeout(() => {
                    resetForm();
                    // Redirecionar para lista de campanhas
                    window.location.href = '/colaborador/campanha';
                }, 2000);
            } else {
                showAlert('Erro', data.message || 'Erro ao criar campanha', 'error');
            }
        })
        .catch(error => {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
            showAlert('Erro', error.message || 'Erro ao criar campanha', 'error');
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
        
        // Resetar datas mínimas
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('data_inicio').min = today;
        document.getElementById('data_fim').min = today;
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
    
    // Utilitários
    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('pt-BR', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        });
    }
    
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    // Animações e efeitos visuais
    function addRippleEffect(element, event) {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s linear;
            pointer-events: none;
        `;
        
        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }
    
    // Adicionar efeito ripple aos botões
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            addRippleEffect(this, e);
        });
    });
    
    // Adicionar animação CSS para ripple
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Salvar rascunho automaticamente (localStorage)
    function saveAsDraft() {
        const draftData = {
            titulo: document.getElementById('titulo').value,
            descricao: document.getElementById('descricao').value,
            data_inicio: document.getElementById('data_inicio').value,
            data_fim: document.getElementById('data_fim').value,
            timestamp: new Date().toISOString()
        };
        
        localStorage.setItem('campanha_rascunho', JSON.stringify(draftData));
    }
    
    function loadDraft() {
        const draft = localStorage.getItem('campanha_rascunho');
        if (draft) {
            const draftData = JSON.parse(draft);
            
            // Verificar se o rascunho não é muito antigo (24 horas)
            const draftAge = new Date() - new Date(draftData.timestamp);
            if (draftAge < 24 * 60 * 60 * 1000) {
                if (confirm('Encontramos um rascunho salvo. Deseja carregá-lo?')) {
                    document.getElementById('titulo').value = draftData.titulo || '';
                    document.getElementById('descricao').value = draftData.descricao || '';
                    document.getElementById('data_inicio').value = draftData.data_inicio || '';
                    document.getElementById('data_fim').value = draftData.data_fim || '';
                }
            }
        }
    }
    
    // Carregar rascunho ao inicializar
    loadDraft();
    
    // Salvar rascunho a cada mudança
    const draftFields = ['titulo', 'descricao', 'data_inicio', 'data_fim'];
    draftFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('input', debounce(saveAsDraft, 1000));
        }
    });
    
    // Função debounce para otimizar salvamento
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Limpar rascunho ao submeter com sucesso
    document.getElementById('successModal').addEventListener('shown.bs.modal', () => {
        localStorage.removeItem('campanha_rascunho');
    });
});

