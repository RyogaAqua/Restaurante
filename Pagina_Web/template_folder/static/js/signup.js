// Define API_URL explícitamente
const API_URL = 'http://127.0.0.1:5000';

document.getElementById('signup-form').addEventListener('submit', async (event) => {
    event.preventDefault(); // Evita que el formulario se envíe de forma predeterminada

    const formData = {
        first_name: document.getElementById('first_name').value,
        last_name: document.getElementById('last_name').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        password: document.getElementById('password').value,
        address: document.getElementById('address').value,
        city: document.getElementById('city').value,
        state: document.getElementById('state').value,
        zip_code: document.getElementById('zip_code').value,
        country: document.getElementById('country').value
    };

    try {
        const response = await fetch('/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();
        if (response.status === 201) {
            alert('User registered successfully!');
        } else {
            alert(result.error || 'Registration failed.');
        }
    } catch (error) {
        console.error('Error during registration:', error);
        alert('An error occurred. Please try again.');
    }
});
