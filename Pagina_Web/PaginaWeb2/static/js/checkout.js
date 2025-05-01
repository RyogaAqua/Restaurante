document.addEventListener('DOMContentLoaded', function() {
    const checkoutBtn = document.querySelector('.checkout-btn');
    const paymentModal = document.getElementById('payment-modal');
    const closeModalBtn = document.querySelector('.close-modal');
    const paymentForm = document.getElementById('payment-form');
    const paymentOptions = document.querySelectorAll('.payment-option');
    const cardForm = document.querySelector('.card-form');
    const paypalForm = document.querySelector('.paypal-form');
    const cashForm = document.querySelector('.cash-form');

    // Actualizar total en tiempo real
    function updateTotal() {
        const cartItems = document.querySelectorAll('.cart-item');
        let subtotal = 0;

        cartItems.forEach(item => {
            const price = parseFloat(item.querySelector('.price').textContent.replace('$', ''));
            const quantity = parseInt(item.querySelector('.quantity-input').value);
            subtotal += price * quantity;
        });

        const tax = subtotal * 0.08; // 8% de impuesto
        const shipping = 5.00; // Cargo fijo de envío
        const total = subtotal + tax + shipping;

        document.getElementById('subtotal').textContent = `$${subtotal.toFixed(2)}`;
        document.getElementById('tax').textContent = `$${tax.toFixed(2)}`;
        document.getElementById('shipping').textContent = `$${shipping.toFixed(2)}`;
        document.getElementById('total').textContent = `$${total.toFixed(2)}`;
        document.getElementById('modal-total').textContent = `$${total.toFixed(2)}`;
    }

    // Mostrar/ocultar modal de pago
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', function() {
            paymentModal.classList.add('show');
            updateTotal();
        });
    }

    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', function() {
            paymentModal.classList.remove('show');
        });
    }

    // Cambiar entre métodos de pago
    paymentOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Remover clase active de todas las opciones
            paymentOptions.forEach(opt => opt.classList.remove('active'));
            // Agregar clase active a la opción seleccionada
            this.classList.add('active');

            // Ocultar todos los formularios
            cardForm.style.display = 'none';
            paypalForm.style.display = 'none';
            cashForm.style.display = 'none';

            // Mostrar el formulario correspondiente
            if (this.dataset.method === 'card') {
                cardForm.style.display = 'block';
            } else if (this.dataset.method === 'paypal') {
                paypalForm.style.display = 'block';
            } else if (this.dataset.method === 'cash') {
                cashForm.style.display = 'block';
            }
        });
    });

    // Validación y envío del formulario de pago
    if (paymentForm) {
        paymentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Aquí iría la lógica de procesamiento de pago
            // Por ahora solo mostraremos un mensaje de éxito
            const successMessage = document.createElement('div');
            successMessage.className = 'success-message';
            successMessage.innerHTML = `
                <i class="fas fa-check-circle"></i>
                <h3>¡Pago Exitoso!</h3>
                <p>Tu pedido ha sido procesado correctamente.</p>
                <p>Recibirás un correo con los detalles de tu compra.</p>
            `;
            
            paymentForm.innerHTML = '';
            paymentForm.appendChild(successMessage);
            
            // Cerrar el modal después de 3 segundos
            setTimeout(() => {
                paymentModal.classList.remove('show');
                // Limpiar el carrito
                document.querySelector('.cart-items').innerHTML = '';
                updateTotal();
            }, 3000);
        });
    }

    // Actualizar total cuando cambie la cantidad
    document.querySelectorAll('.quantity-btn').forEach(btn => {
        btn.addEventListener('click', updateTotal);
    });
});
