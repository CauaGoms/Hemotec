// Animação de contadores
function animateCounters() {
    const counters = document.querySelectorAll(".stats-number");

    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute("data-target"));
        const increment = target / 100;
        let current = 0;

        const updateCounter = () => {
            if (current < target) {
                current += increment;
                counter.textContent = Math.floor(current).toLocaleString();
                setTimeout(updateCounter, 20);
            } else {
                counter.textContent = target.toLocaleString();
            }
        };

        updateCounter();
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
            if (entry.target.classList.contains("stats-section")) {
                animateCounters();
            }
            entry.target.classList.add("visible");
        }
    });
}, observerOptions);

// Observar elementos para animação
document.querySelectorAll(".fade-in").forEach(el => {
    observer.observe(el);
});

// Smooth scrolling para links internos
document.querySelectorAll("a[href^='#']").forEach(anchor => {
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

// Inicializar animações na carga da página
document.addEventListener("DOMContentLoaded", () => {
    handleScrollAnimations();
    handleNavbarScroll();
});