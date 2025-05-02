// Define API_URL explícitamente
const API_URL = 'http://127.0.0.1:5000';

document.getElementById('signup-form').addEventListener('submit', async (event) => {
    event.preventDefault(); // Evita que el formulario se envíe de forma predeterminada

    const formData = {
        nombre_usuario: document.getElementById('nombre_usuario').value,
        apellido_usuario: document.getElementById('apellido_usuario').value,
        email: document.getElementById('email').value,
        telefono: document.getElementById('telefono').value,
        contrasena: document.getElementById('contrasena').value,
        metodo_pago: document.getElementById('metodo_pago').value,
        address: {
            address: document.getElementById('address').value,
            city: document.getElementById('city').value,
            state: document.getElementById('state').value,
            zip_code: document.getElementById('zip_code').value,
            country: document.getElementById('country').value
        }
    };

    try {
        const response = await fetch('/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            const result = await response.json();
            alert(result.message);
            window.location.href = 'signin.html'; // Redirige al inicio de sesión
        } else {
            const error = await response.json();
            alert(`Error: ${error.error}`);
        }
    } catch (err) {
        console.error('Error al registrar el usuario:', err);
        alert('Ocurrió un error al registrar el usuario. Por favor, inténtalo de nuevo.');
    }
});
