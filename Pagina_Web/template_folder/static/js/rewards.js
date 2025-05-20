// Función para calcular puntos basado en el precio
function calculatePoints(price) {
    return Math.floor(price * 10); // 10 puntos por cada dólar
}

// Función para actualizar los puntos mostrados
function updateCartPoints() {
    const cartItems = document.querySelectorAll('.cart-item');
    let totalPoints = 0;

    cartItems.forEach(item => {
        const priceText = item.querySelector('.price').textContent;
        const price = parseFloat(priceText.replace('$', ''));
        const quantity = parseInt(item.querySelector('.quantity-input').value);
        totalPoints += calculatePoints(price * quantity);
    });

    const cartPointsElement = document.getElementById('cart-points');
    if (cartPointsElement) {
        cartPointsElement.textContent = totalPoints.toLocaleString();
    }
}

// Agregar evento a los botones de agregar al carrito
document.addEventListener('DOMContentLoaded', function() {
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const card = this.closest('.product-card, .category-card');
            const priceText = card.querySelector('.price').textContent;
            const price = parseFloat(priceText.replace('$', ''));
            const points = calculatePoints(price);
            
            // Actualizar puntos en tiempo real
            const currentPoints = parseInt(document.getElementById('cart-points').textContent.replace(',', ''));
            document.getElementById('cart-points').textContent = (currentPoints + points).toLocaleString();
            
            // Mostrar notificación
            showNotification(`¡${points} puntos agregados!`);
        });
    });
});

// Función para mostrar notificación
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'points-notification';
    notification.innerHTML = `
        <i class="fas fa-coins"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    // Animar entrada
    setTimeout(() => notification.classList.add('show'), 100);
    
    // Remover después de 3 segundos
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}
