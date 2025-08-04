// Validação do formulário de contato
function initializeFormValidation() {
    const form = document.getElementById("contactForm");
    const successMessage = document.getElementById("successMessage");

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        if (form.checkValidity()) {
            // Simular envio de formulário
            console.log("Formulário enviado:");
            console.log("Nome:", form.name.value);
            console.log("Email:", form.email.value);
            console.log("Telefone:", form.phone.value);
            console.log("Assunto:", form.subject.value);
            console.log("Mensagem:", form.message.value);

            successMessage.style.display = "block";
            form.reset();
            setTimeout(() => {
                successMessage.style.display = "none";
            }, 5000);
        } else {
            form.classList.add("was-validated");
        }
    });
}

// Animação de fade-in ao scroll
function handleScrollAnimations() {
    const elements = document.querySelectorAll(".fade-in");

    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;

        if (elementTop < window.innerHeight - elementVisible) {
            element.classList.add("visible");
        }
    });
}

// Navbar scroll effect
function handleNavbarScroll() {
    const navbar = document.querySelector(".navbar");
    if (window.scrollY > 50) {
        navbar.style.backgroundColor = "rgba(255, 255, 255, 0.95)";
        navbar.style.backdropFilter = "blur(10px)";
    } else {
        navbar.style.backgroundColor = "white";
        navbar.style.backdropFilter = "none";
    }
}

// Event listeners
window.addEventListener("scroll", () => {
    handleScrollAnimations();
    handleNavbarScroll();
});

// Intersection Observer para animações mais suaves
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

// Observar elementos para animação
document.querySelectorAll(".fade-in").forEach(el => {
    observer.observe(el);
});

// Smooth scrolling para links internos
document.querySelectorAll("a[href^=\"#\"]").forEach(anchor => {
    anchor.addEventListener("click", function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute("href"));
        if (target) {
            target.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        }
    });
});

// Inicializar funcionalidades na carga da página
document.addEventListener("DOMContentLoaded", () => {
    initializeFormValidation();
    handleScrollAnimations();
    handleNavbarScroll();
});