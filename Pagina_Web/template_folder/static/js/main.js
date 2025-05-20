// Cart functionality for Add to Cart buttons
document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', () => {
        const productCard = button.closest('.product-card');
        const item = {
            id: Math.random().toString(36).substr(2, 9), // Generate a random ID
            name: productCard.querySelector('h3').textContent,
            price: parseFloat(productCard.querySelector('.price').textContent.replace('$', ''))
        };
        
        // Add item to cart
        const cart = JSON.parse(localStorage.getItem('cart') || '[]');
        const existingItem = cart.find(i => i.name === item.name);
        
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            cart.push({ ...item, quantity: 1 });
        }
        
        localStorage.setItem('cart', JSON.stringify(cart));
        
        // Show notification
        showNotification('Item added to cart!');
    });
});

// Gallery filters
const galleryFilters = document.querySelector('.gallery-filters');
const galleryItems = document.querySelectorAll('.gallery-item');

if (galleryFilters) {
    galleryFilters.addEventListener('click', (e) => {
        if (e.target.classList.contains('filter-btn')) {
            // Remove active class from all buttons
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active');
            });

            // Add active class to clicked button
            e.target.classList.add('active');

            // Get selected category
            const category = e.target.dataset.filter;

            // Filter gallery items
            galleryItems.forEach(item => {
                if (category === 'all' || item.dataset.category === category) {
                    item.style.display = 'block';
                    item.style.animation = 'scaleIn 0.5s ease-out forwards';
                } else {
                    item.style.display = 'none';
                }
            });
        }
    });
}

// Contact form handling
const contactForm = document.getElementById('contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = {
            name: this.querySelector('#name').value,
            email: this.querySelector('#email').value,
            subject: this.querySelector('#subject').value,
            message: this.querySelector('#message').value
        };

        // Here you would typically send this to your backend
        console.log('Form submission:', formData);
        showNotification('Message sent successfully!');
        this.reset();
    });
}

// Enhanced notification system
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="${type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'}"></i>
            <p>${message}</p>
        </div>
        <button class="notification-close"><i class="fas fa-times"></i></button>
    `;

    document.body.appendChild(notification);

    // Add animation class after a small delay
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);

    // Close button functionality
    notification.querySelector('.notification-close').addEventListener('click', () => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    });

    // Auto close after 5 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 5000);
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    // Menu filtering
    const categoryButtons = document.querySelectorAll('.category-btn');
    const menuItems = document.querySelectorAll('.menu-item');

    if (categoryButtons.length > 0) {
        categoryButtons.forEach(button => {
            button.addEventListener('click', () => {
                // Remove active class from all buttons
                categoryButtons.forEach(btn => btn.classList.remove('active'));
                // Add active class to clicked button
                button.classList.add('active');

                const category = button.dataset.category;

                menuItems.forEach(item => {
                    if (category === 'all' || item.dataset.category === category) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                });
            });
        });
    }
    const mobileMenu = document.getElementById('mobile-menu');
    const navMenu = document.querySelector('.nav-menu');

    mobileMenu.addEventListener('click', function() {
        navMenu.classList.toggle('active');
        this.classList.toggle('active');
    });

    // Cart functionality
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    let cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const card = this.closest('.product-card');
            const product = {
                name: card.querySelector('h3').textContent,
                price: parseFloat(card.querySelector('.price').textContent.replace('$', '')),
                quantity: 1
            };

            // Check if product already exists in cart
            const existingProduct = cartItems.find(item => item.name === product.name);
            if (existingProduct) {
                existingProduct.quantity += 1;
            } else {
                cartItems.push(product);
            }

            // Save to localStorage
            localStorage.setItem('cartItems', JSON.stringify(cartItems));

            // Show notification
            showNotification('Item added to cart!');
        });
    });

    // Newsletter form
    const newsletterForm = document.getElementById('newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            // Here you would typically send this to your backend
            showNotification('Thank you for subscribing!');
            this.reset();
        });
    }
});

// Notification function
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #10b981;
        color: white;
        padding: 1rem 2rem;
        border-radius: 5px;
        animation: slideIn 0.5s ease-out forwards;
        z-index: 1000;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.5s ease-out forwards';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 500);
    }, 3000);
}

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Auth form handling
const signinForm = document.getElementById('signin-form');
if (signinForm) {
    signinForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const email = this.querySelector('#email').value;
        const password = this.querySelector('#password').value;

        fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Login failed');
            }
            return response.json();
        })
        .then(data => {
            showNotification('Login successful!', 'success');
        })
        .catch(error => {
            showNotification('Login failed. Please check your credentials.', 'error');
        });
    });

    // Password visibility toggle
    const togglePassword = document.querySelector('.toggle-password');
    const passwordInput = document.querySelector('#password');

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            this.querySelector('i').classList.toggle('fa-eye');
            this.querySelector('i').classList.toggle('fa-eye-slash');
        });
    }
}

// Lazy loading for images
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('[data-src]');
    const imageOptions = {
        threshold: 0,
        rootMargin: '0px 0px 50px 0px'
    };

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('fade-in');
                observer.unobserve(img);
            }
        });
    }, imageOptions);

    images.forEach(img => imageObserver.observe(img));
});

// Verificar el estado de autenticación y actualizar los botones de Sign In y Sign Out
document.addEventListener('DOMContentLoaded', () => {
    fetch('/auth/status')
        .then(response => response.json())
        .then(data => {
            if (data.isAuthenticated) {
                document.getElementById('signout-button').style.display = 'inline-block';
                document.querySelector('.signin-btn').style.display = 'none';
            } else {
                document.getElementById('signout-button').style.display = 'none';
                document.querySelector('.signin-btn').style.display = 'inline-block';
            }
        })
        .catch(error => console.error('Error al verificar el estado de autenticación:', error));
});

// Agregar evento al botón de Sign Out
document.getElementById('signout-button').addEventListener('click', (e) => {
    e.preventDefault();
    fetch('/auth/logout', { method: 'POST' })
        .then(response => {
            if (response.ok) {
                // Actualizar el estado de los botones
                document.getElementById('signout-button').style.display = 'none';
                document.querySelector('.signin-btn').style.display = 'inline-block';
                alert('Has cerrado sesión exitosamente.');
            } else {
                alert('Error al cerrar sesión.');
            }
        })
        .catch(error => console.error('Error al cerrar sesión:', error));
});
