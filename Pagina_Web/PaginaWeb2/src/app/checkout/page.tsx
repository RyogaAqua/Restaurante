import { useState } from 'react';
import { createOrder } from '@/utils/api';

export default function CheckoutPage() {
  const [cart, setCart] = useState<any[]>([]); // Simula el carrito
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  async function handleCheckout() {
    try {
      const orderData = {
        user_id: 1, // Reemplazar con el ID del usuario autenticado
        restaurant_id: 1, // Reemplazar con el ID del restaurante
        items: cart.map((item) => ({
          id_objeto: item.id,
          quantity: item.quantity,
        })),
        address: {
          address: '123 Main St',
          city: 'City',
          state: 'State',
          zip_code: '12345',
          country: 'Country',
        },
      };
      const response = await createOrder(orderData);
      setSuccess('Order created successfully!');
    } catch (err) {
      setError('Failed to create order');
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-8">Checkout</h1>
      {error && <div className="text-red-500">{error}</div>}
      {success && <div className="text-green-500">{success}</div>}
      <button onClick={handleCheckout} className="bg-primary text-white py-2 px-4 rounded">
        Place Order
      </button>
    </div>
  );
}
