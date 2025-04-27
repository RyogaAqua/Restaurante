document.getElementById('signup-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const formData = {
        nombre_usuario: document.getElementById('nombre_usuario').value,
        apellido_usuario: document.getElementById('apellido_usuario').value,
        email: document.getElementById('email').value,
        telefono: document.getElementById('telefono').value,
        contrasena: document.getElementById('contrasena').value,
        address: {
            address: document.getElementById('address').value,
            city: document.getElementById('city').value,
            state: document.getElementById('state').value,
            zip_code: document.getElementById('zip_code').value,
            country: document.getElementById('country').value,
        },
        metodo_pago: document.getElementById('metodo_pago').value,
    };

    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData),
        });

        if (!response.ok) {
            throw new Error('Failed to register');
        }

        const data = await response.json();
        alert('Registration successful! You can now sign in.');
        window.location.href = 'signin.html';
    } catch (error) {
        alert('Error during registration: ' + error.message);
    }
});
