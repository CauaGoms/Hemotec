// Gestão de Administradores - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Search functionality
    const searchInput = document.getElementById('searchInput');
    const adminCards = document.querySelectorAll('.admin-card');
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            
            adminCards.forEach(card => {
                const name = card.querySelector('.admin-name').textContent.toLowerCase();
                const email = card.querySelector('.meta-item span').textContent.toLowerCase();
                
                if (name.includes(searchTerm) || email.includes(searchTerm)) {
                    card.closest('.col-md-4').style.display = '';
                    card.classList.add('fade-in');
                } else {
                    card.closest('.col-md-4').style.display = 'none';
                }
            });
            
            updateEmptyState();
        });
    }
    
    // Filter functionality
    const filterBtns = document.querySelectorAll('.filter-btn');
    
    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove active class from all buttons
            filterBtns.forEach(b => b.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            const filter = this.getAttribute('data-filter');
            
            adminCards.forEach(card => {
                const status = card.querySelector('.admin-status');
                
                if (filter === 'all') {
                    card.closest('.col-md-4').style.display = '';
                } else if (filter === 'active') {
                    if (status && status.classList.contains('status-active')) {
                        card.closest('.col-md-4').style.display = '';
                    } else {
                        card.closest('.col-md-4').style.display = 'none';
                    }
                } else if (filter === 'inactive') {
                    if (status && status.classList.contains('status-inactive')) {
                        card.closest('.col-md-4').style.display = '';
                    } else {
                        card.closest('.col-md-4').style.display = 'none';
                    }
                }
            });
            
            updateEmptyState();
        });
    });
    
    // Update empty state
    function updateEmptyState() {
        const visibleCards = Array.from(adminCards).filter(card => {
            return card.closest('.col-md-4').style.display !== 'none';
        });
        
        const emptyState = document.querySelector('.empty-state');
        const adminGrid = document.querySelector('.row');
        
        if (visibleCards.length === 0) {
            if (!emptyState) {
                const empty = document.createElement('div');
                empty.className = 'col-12 empty-state';
                empty.innerHTML = `
                    <div class="text-center py-5">
                        <i class="fas fa-user-slash fa-5x text-muted mb-3"></i>
                        <h4 class="text-muted">Nenhum administrador encontrado</h4>
                        <p class="text-muted">Tente ajustar os filtros de busca</p>
                    </div>
                `;
                adminGrid.appendChild(empty);
            }
        } else {
            if (emptyState) {
                emptyState.remove();
            }
        }
    }
    
    // Animate cards on load
    adminCards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in');
        }, index * 100);
    });
    
    // Delete confirmation
    const deleteBtns = document.querySelectorAll('.btn-admin-delete');
    
    deleteBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            const adminName = this.closest('.admin-card').querySelector('.admin-name').textContent;
            
            if (!confirm(`Tem certeza que deseja excluir o administrador "${adminName}"?`)) {
                e.preventDefault();
            }
        });
    });
});
