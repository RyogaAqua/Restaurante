'use client';

import { useEffect, useState } from 'react';
import { getCart, saveCart } from '@/utils/api';

export default function CartPage() {
  const [cartItems, setCartItems] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadCart() {
      try {
        const userId = localStorage.getItem('userId'); // Asegúrate de guardar el ID del usuario al iniciar sesión
        if (!userId) {
          setError('User not logged in');
          return;
        }

        const data = await getCart(Number(userId));
        setCartItems(data.cart_items);
      } catch (err: any) {
        setError(err.message);
      }
    }

    loadCart();
  }, []);

  async function handleSaveCart() {
    try {
      const userId = localStorage.getItem('userId');
      if (!userId) {
        setError('User not logged in');
        return;
      }

      await saveCart(Number(userId), cartItems);
      alert('Cart saved successfully!');
    } catch (err: any) {
      setError(err.message);
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-8">Your Cart</h1>
      {error && <div className="text-red-500">{error}</div>}
      <div>
        {cartItems.map((item) => (
          <div key={item.id_objeto} className="flex items-center justify-between mb-4">
            <span>{item.nombre_objeto}</span>
            <span>{item.quantity}</span>
            <span>${item.precio.toFixed(2)}</span>
          </div>
        ))}
      </div>
      <button onClick={handleSaveCart} className="bg-primary text-white py-2 px-4 rounded">
        Save Cart
      </button>
    </div>
  );
}
