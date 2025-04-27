'use client';

import { useState } from 'react';
import { updateStock, checkAvailability } from '@/utils/api';

export default function InventoryPage() {
  const [itemId, setItemId] = useState('');
  const [quantity, setQuantity] = useState('');
  const [availability, setAvailability] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  async function handleUpdateStock() {
    try {
      if (!itemId || !quantity) {
        setError('Please provide both item ID and quantity');
        return;
      }

      await updateStock(Number(itemId), Number(quantity));
      setError(null);
      alert('Stock updated successfully!');
    } catch (err: any) {
      setError(err.message);
    }
  }

  async function handleCheckAvailability() {
    try {
      const items = [{ item_id: Number(itemId), quantity: Number(quantity) }];
      const data = await checkAvailability(items);
      setAvailability(data.availability);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-8">Inventory Management</h1>
      {error && <div className="text-red-500">{error}</div>}
      <div className="space-y-4">
        <div>
          <label htmlFor="itemId">Item ID</label>
          <input
            type="text"
            id="itemId"
            value={itemId}
            onChange={(e) => setItemId(e.target.value)}
            className="w-full border p-2 rounded"
          />
        </div>
        <div>
          <label htmlFor="quantity">Quantity</label>
          <input
            type="text"
            id="quantity"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            className="w-full border p-2 rounded"
          />
        </div>
        <button
          onClick={handleUpdateStock}
          className="bg-primary text-white py-2 px-4 rounded"
        >
          Update Stock
        </button>
        <button
          onClick={handleCheckAvailability}
          className="bg-secondary text-white py-2 px-4 rounded"
        >
          Check Availability
        </button>
      </div>
      {availability.length > 0 && (
        <div className="mt-8">
          <h2 className="text-2xl font-bold mb-4">Availability</h2>
          <ul>
            {availability.map((item) => (
              <li key={item.item_id}>
                Item ID: {item.item_id} - {item.available ? 'Available' : `Unavailable (${item.message})`}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
