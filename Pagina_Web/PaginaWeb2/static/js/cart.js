// Initialize cart in localStorage if it doesn't exist
if (!localStorage.getItem('cart')) {
    localStorage.setItem('cart', JSON.stringify([]));
}

// Cart management
class Cart {
    static getCart() {
        return JSON.parse(localStorage.getItem('cart')) || [];
    }

    static addItem(item) {
        const cart = this.getCart();
        const existingItem = cart.find(i => i.id === item.id);
        
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            cart.push({ ...item, quantity: 1 });
        }
        
        localStorage.setItem('cart', JSON.stringify(cart));
        this.updateCartDisplay();
    }

    static removeItem(itemId) {
        const cart = this.getCart();
        const updatedCart = cart.filter(item => item.id !== itemId);
        localStorage.setItem('cart', JSON.stringify(updatedCart));
        this.updateCartDisplay();
    }

    static updateQuantity(itemId, quantity) {
        const cart = this.getCart();
        const item = cart.find(i => i.id === itemId);
        if (item) {
            item.quantity = parseInt(quantity);
            if (item.quantity <= 0) {
                this.removeItem(itemId);
            } else {
                localStorage.setItem('cart', JSON.stringify(cart));
                this.updateCartDisplay();
            }
        }
    }

    static calculateTotals() {
        const cart = this.getCart();
        const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        const tax = subtotal * 0.10; // 10% tax
        const total = subtotal + tax;
        
        return {
            subtotal: subtotal.toFixed(2),
            tax: tax.toFixed(2),
            total: total.toFixed(2)
        };
    }

    static updateCartDisplay() {
        const cartItemsContainer = document.getElementById('cart-items');
        const cart = this.getCart();
        
        if (!cartItemsContainer) return;

        cartItemsContainer.innerHTML = '';
        
        if (cart.length === 0) {
            cartItemsContainer.innerHTML = '<p class="empty-cart">Your cart is empty</p>';
            return;
        }

        cart.forEach(item => {
            const itemElement = document.createElement('div');
            itemElement.className = 'cart-item';
            itemElement.innerHTML = `
                <div class="item-details">
                    <h4>${item.name}</h4>
                    <p class="price">$${item.price}</p>
                </div>
                <div class="item-quantity">
                    <button class="quantity-btn minus" data-id="${item.id}">-</button>
                    <input type="number" value="${item.quantity}" min="1" data-id="${item.id}">
                    <button class="quantity-btn plus" data-id="${item.id}">+</button>
                </div>
                <button class="remove-item" data-id="${item.id}">
                    <i class="fas fa-trash"></i>
                </button>
            `;
            cartItemsContainer.appendChild(itemElement);
        });

        // Update totals
        const totals = this.calculateTotals();
        document.getElementById('cart-subtotal').textContent = `$${totals.subtotal}`;
        document.getElementById('cart-tax').textContent = `$${totals.tax}`;
        document.getElementById('cart-total').textContent = `$${totals.total}`;
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    Cart.updateCartDisplay();

    // Handle quantity changes and item removal
    document.getElementById('cart-items')?.addEventListener('click', (e) => {
        const itemId = e.target.dataset.id;
        if (!itemId) return;

        if (e.target.classList.contains('minus')) {
            const currentItem = Cart.getCart().find(item => item.id === itemId);
            if (currentItem) {
                Cart.updateQuantity(itemId, currentItem.quantity - 1);
            }
        } else if (e.target.classList.contains('plus')) {
            const currentItem = Cart.getCart().find(item => item.id === itemId);
            if (currentItem) {
                Cart.updateQuantity(itemId, currentItem.quantity + 1);
            }
        } else if (e.target.classList.contains('remove-item') || e.target.closest('.remove-item')) {
            Cart.removeItem(itemId);
        }
    });

    // Handle quantity input changes
    document.getElementById('cart-items')?.addEventListener('change', (e) => {
        if (e.target.tagName === 'INPUT' && e.target.type === 'number') {
            const itemId = e.target.dataset.id;
            Cart.updateQuantity(itemId, e.target.value);
        }
    });

    // Payment method selection
    const paymentOptions = document.querySelectorAll('.payment-option');
    paymentOptions.forEach(option => {
        option.addEventListener('click', () => {
            paymentOptions.forEach(opt => opt.classList.remove('active'));
            option.classList.add('active');
            
            const paymentMethod = option.dataset.payment;
            const cardElement = document.getElementById('card-element');
            
            if (paymentMethod === 'card') {
                cardElement.style.display = 'block';
                // Initialize Stripe elements here
                const stripe = Stripe('your_publishable_key'); // Replace with your Stripe key
                const elements = stripe.elements();
                const card = elements.create('card');
                card.mount('#card-element');
            } else {
                cardElement.style.display = 'none';
            }
        });
    });

    // Checkout button
    document.getElementById('checkout-button')?.addEventListener('click', async (e) => {
        e.preventDefault();
        
        // Validate address form
        const addressForm = document.getElementById('address-form');
        if (!addressForm.checkValidity()) {
            addressForm.reportValidity();
            return;
        }

        const activePaymentMethod = document.querySelector('.payment-option.active');
        if (!activePaymentMethod) {
            alert('Please select a payment method');
            return;
        }

        // Here you would typically send the order to your backend
        // For demonstration, we'll just show a success message
        alert('Order placed successfully!');
        localStorage.setItem('cart', JSON.stringify([]));
        Cart.updateCartDisplay();
    });
});
