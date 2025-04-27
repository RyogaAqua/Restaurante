'use client';

import { useState } from 'react';
import { getDeliveryStatus } from '@/utils/api';

export default function DeliveryStatusPage() {
  const [orderId, setOrderId] = useState('');
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleTrackOrder() {
    try {
      if (!orderId) {
        setError('Please enter a valid order ID');
        return;
      }

      const data = await getDeliveryStatus(Number(orderId));
      setStatus(data.status);
      setError(null);
    } catch (err: any) {
      setError(err.message);
      setStatus(null);
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-8">Track Your Order</h1>
      <div className="space-y-4">
        <input
          type="text"
          placeholder="Enter your order ID"
          value={orderId}
          onChange={(e) => setOrderId(e.target.value)}
          className="w-full border p-2 rounded"
        />
        <button
          onClick={handleTrackOrder}
          className="bg-primary text-white py-2 px-4 rounded"
        >
          Track Order
        </button>
      </div>
      {status && (
        <div className="mt-8 p-4 bg-green-100 text-green-800 rounded">
          <p>Order Status: <strong>{status}</strong></p>
        </div>
      )}
      {error && (
        <div className="mt-8 p-4 bg-red-100 text-red-800 rounded">
          <p>Error: {error}</p>
        </div>
      )}
    </div>
  );
}
