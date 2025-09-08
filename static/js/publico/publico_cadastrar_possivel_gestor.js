// JS para navegação entre etapas do formulário multi-step

document.addEventListener('DOMContentLoaded', function () {
    const steps = document.querySelectorAll('.form-step');
    let currentStep = 0;

    function showStep(index) {
        steps.forEach((step, i) => {
            step.classList.toggle('active', i === index);
        });
        currentStep = index;
    }

    window.nextStep = function () {
        // Validação simples dos campos obrigatórios
        const activeStep = steps[currentStep];
        const requiredFields = activeStep.querySelectorAll('[required]');
        for (let field of requiredFields) {
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                field.focus();
                return;
            } else {
                field.classList.remove('is-invalid');
            }
        }
        if (currentStep < steps.length - 1) {
            showStep(currentStep + 1);
        }
    };

    window.prevStep = function () {
        if (currentStep > 0) {
            showStep(currentStep - 1);
        }
    };

    // Inicializa mostrando o primeiro passo
    showStep(0);
});
