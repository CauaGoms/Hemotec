document.addEventListener("DOMContentLoaded", function( ) {
        const settingsForm = document.getElementById("profileForm");
        const floatingSaveBtn = document.getElementById("floatingSaveBtn");
        let hasChanges = false;

        function showToast(message, type = "info") {
            const toastContainer = document.getElementById("toastContainer");
            const toast = document.createElement("div");
            toast.className = `toast-notification toast-${type}`;
            toast.innerHTML = `
                <i class="fas fa-${type === "success" ? "check-circle" : type === "error" ? "times-circle" : "info-circle"} me-2"></i>
                ${message}
            `;
            toastContainer.appendChild(toast);

            setTimeout(() => {
                toast.classList.add("show");
            }, 100);

            setTimeout(() => {
                toast.classList.remove("show");
                toast.addEventListener("transitionend", () => toast.remove());
            }, 3000);
        }

        function markAsChanged() {
            if (!hasChanges) {
                hasChanges = true;
                floatingSaveBtn.style.display = "block";
            }
        }

        function markAsSaved() {
            hasChanges = false;
            floatingSaveBtn.style.display = "none";
        }

        // Event listeners para detectar mudanças nos formulários
        document.querySelectorAll(".settings-content input, .settings-content select, .settings-content textarea").forEach(element => {
            element.addEventListener("change", markAsChanged);
            element.addEventListener("keyup", markAsChanged);
        });

        // Listener para o botão flutuante de salvar
        floatingSaveBtn.addEventListener("click", function() {
            // Aqui você pode adicionar a lógica para salvar todas as configurações
            // Por exemplo, coletar dados de todos os formulários e enviar via AJAX
            showToast("Configurações salvas com sucesso!", "success");
            markAsSaved();
        });

        // Funções de exemplo para as ações dos botões
        window.changeProfilePhoto = function() {
            showToast("Abrindo seletor de fotos... (Funcionalidade em desenvolvimento)", "info");
        };

        window.resetProfileForm = function() {
            // Lógica para resetar o formulário de perfil
            document.getElementById("profileForm").reset();
            showToast("Formulário de perfil resetado.", "info");
            markAsSaved();
        };

        window.downloadMyData = function() {
            showToast("Solicitação de download de dados enviada. Você receberá um email em breve. (Funcionalidade em desenvolvimento)", "success");
        };

        window.correctMyData = function() {
            showToast("Redirecionando para o formulário de correção de dados... (Funcionalidade em desenvolvimento)", "info");
        };

        window.deleteMyAccount = function() {
            if (confirm("Tem certeza que deseja excluir sua conta? Esta ação é irreversível.")) {
                showToast("Sua solicitação de exclusão de conta foi enviada. (Funcionalidade em desenvolvimento)", "warning");
            }
        };

        window.changePassword = function() {
            const currentPass = document.getElementById("currentPassword").value;
            const newPass = document.getElementById("newPassword").value;
            const confirmNewPass = document.getElementById("confirmNewPassword").value;

            if (newPass !== confirmNewPass) {
                showToast("As novas senhas não coincidem!", "error");
                return;
            }
            if (newPass.length < 8) {
                showToast("A nova senha deve ter no mínimo 8 caracteres!", "error");
                return;
            }
            // Lógica para alterar a senha
            showToast("Senha alterada com sucesso!", "success");
            document.getElementById("currentPassword").value = "";
            document.getElementById("newPassword").value = "";
            document.getElementById("confirmNewPassword").value = "";
            markAsSaved();
        };

        window.setupTwoFactorAuth = function() {
            showToast("Iniciando configuração de Autenticação de Dois Fatores... (Funcionalidade em desenvolvimento)", "info");
        };

        window.logoutSession = function(device) {
            showToast(`Sessão em ${device} encerrada. (Funcionalidade em desenvolvimento)`, "info");
        };

        window.logoutAllSessions = function() {
            if (confirm("Tem certeza que deseja sair de todas as sessões ativas?")) {
                showToast("Você saiu de todas as sessões. (Funcionalidade em desenvolvimento)", "success");
            }
        };

        // Animação de fade-in ao scroll
        const observerOptions = {
            threshold: 0.1,
            rootMargin: "0px 0px -50px 0px"
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                }
            });
        }, observerOptions);

        document.querySelectorAll(".fade-in").forEach(el => {
            observer.observe(el);
        });

        // Navbar scroll effect (se houver navbar fixa)
        function handleNavbarScroll() {
            const navbar = document.querySelector(".navbar");
            if (navbar) {
                if (window.scrollY > 50) {
                    navbar.style.backgroundColor = "rgba(255, 255, 255, 0.95)";
                    navbar.style.backdropFilter = "blur(10px)";
                } else {
                    navbar.style.backgroundColor = "white";
                    navbar.style.backdropFilter = "none";
                }
            }
        }

        window.addEventListener("scroll", handleNavbarScroll);

        // Inicializar na carga da página
        handleNavbarScroll();
    });