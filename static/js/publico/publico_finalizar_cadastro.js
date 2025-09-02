// Script para navegação entre etapas do cadastro de gestor
document.addEventListener('DOMContentLoaded', function() {
	let currentStep = 1;
	const totalSteps = 3;
	const sections = [
		document.getElementById('cadastroSection1'),
		document.getElementById('cadastroSection2'),
		document.getElementById('cadastroSection3')
	];
	const prevBtn = document.getElementById('cadastroPrevBtn');
	const nextBtn = document.getElementById('cadastroNextBtn');
	const submitBtn = document.getElementById('cadastroSubmitBtn');

	function showStep(step) {
		sections.forEach((section, idx) => {
			section.style.display = (idx === step - 1) ? 'block' : 'none';
		});
		prevBtn.style.display = (step > 1) ? 'inline-block' : 'none';
		nextBtn.style.display = (step < totalSteps) ? 'inline-block' : 'none';
		submitBtn.style.display = (step === totalSteps) ? 'inline-block' : 'none';
	}

	window.cadastroChangeStep = function(direction) {
		currentStep += direction;
		if (currentStep < 1) currentStep = 1;
		if (currentStep > totalSteps) currentStep = totalSteps;
		showStep(currentStep);
	};

	showStep(currentStep);
});
