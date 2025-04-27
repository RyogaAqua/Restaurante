'use client';

import { useEffect, useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default function OrderHistoryPage() {
  const [orders, setOrders] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchOrderHistory() {
      try {
        const userId = localStorage.getItem('userId'); // Asegúrate de guardar el ID del usuario al iniciar sesión
        if (!userId) {
          setError('User not logged in');
          return;
        }

        const response = await fetch(`${API_URL}/orders/history?user_id=${userId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch order history');
        }

        const data = await response.json();
        setOrders(data.orders);
      } catch (err: any) {
        setError(err.message);
      }
    }

    fetchOrderHistory();
  }, []);

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-8">Order History</h1>
      {orders.length === 0 ? (
        <p>No orders found.</p>
      ) : (
        <div className="space-y-8">
          {orders.map((order) => (
            <div key={order.id_transaccion} className="bg-white rounded-lg shadow p-4">
              <h2 className="text-xl font-bold">Order #{order.id_transaccion}</h2>
              <p className="text-gray-600">Date: {order.fecha_orden}</p>
              <p className="text-gray-600">Total: ${order.precio_total.toFixed(2)}</p>
              <p className="text-gray-600">Points Earned: {order.puntos_ganados}</p>
              <p className="text-gray-600">Points Spent: {order.puntos_gastados}</p>
              <h3 className="text-lg font-bold mt-4">Items:</h3>
              <ul className="list-disc pl-5">
                {order.items.map((item) => (
                  <li key={item.id_objeto}>
                    {item.nombre_objeto} - {item.quantity} x ${item.precio_unitario.toFixed(2)}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
