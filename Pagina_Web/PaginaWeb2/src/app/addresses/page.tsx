'use client';

import { useEffect, useState } from 'react';
import { addAddress, listAddresses, deleteAddress } from '@/utils/api';

export default function AddressesPage() {
  const [addresses, setAddresses] = useState<any[]>([]);
  const [newAddress, setNewAddress] = useState({
    address: '',
    city: '',
    state: '',
    zip_code: '',
    country: '',
  });
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadAddresses() {
      try {
        const userId = localStorage.getItem('userId'); // Asegúrate de guardar el ID del usuario al iniciar sesión
        if (!userId) {
          setError('User not logged in');
          return;
        }

        const data = await listAddresses(Number(userId));
        setAddresses(data.addresses);
      } catch (err: any) {
        setError(err.message);
      }
    }

    loadAddresses();
  }, []);

  async function handleAddAddress() {
    try {
      const userId = localStorage.getItem('userId');
      if (!userId) {
        setError('User not logged in');
        return;
      }

      const data = await addAddress(Number(userId), newAddress);
      setAddresses((prev) => [...prev, data.address]);
      setNewAddress({ address: '', city: '', state: '', zip_code: '', country: '' });
    } catch (err: any) {
      setError(err.message);
    }
  }

  async function handleDeleteAddress(addressId: number) {
    try {
      await deleteAddress(addressId);
      setAddresses((prev) => prev.filter((address) => address.id_address !== addressId));
    } catch (err: any) {
      setError(err.message);
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-8">Manage Addresses</h1>
      {error && <div className="text-red-500">{error}</div>}
      <div className="space-y-4">
        {addresses.map((address) => (
          <div key={address.id_address} className="bg-white rounded-lg shadow p-4">
            <p>{address.address}</p>
            <p>{address.city}, {address.state}, {address.zip_code}, {address.country}</p>
            <button
              onClick={() => handleDeleteAddress(address.id_address)}
              className="text-red-500 hover:underline"
            >
              Delete
            </button>
          </div>
        ))}
      </div>
      <div className="mt-8">
        <h2 className="text-xl font-bold mb-4">Add New Address</h2>
        <div className="space-y-4">
          <input
            type="text"
            placeholder="Address"
            value={newAddress.address}
            onChange={(e) => setNewAddress({ ...newAddress, address: e.target.value })}
            className="w-full border p-2 rounded"
          />
          <input
            type="text"
            placeholder="City"
            value={newAddress.city}
            onChange={(e) => setNewAddress({ ...newAddress, city: e.target.value })}
            className="w-full border p-2 rounded"
          />
          <input
            type="text"
            placeholder="State"
            value={newAddress.state}
            onChange={(e) => setNewAddress({ ...newAddress, state: e.target.value })}
            className="w-full border p-2 rounded"
          />
          <input
            type="text"
            placeholder="Zip Code"
            value={newAddress.zip_code}
            onChange={(e) => setNewAddress({ ...newAddress, zip_code: e.target.value })}
            className="w-full border p-2 rounded"
          />
          <input
            type="text"
            placeholder="Country"
            value={newAddress.country}
            onChange={(e) => setNewAddress({ ...newAddress, country: e.target.value })}
            className="w-full border p-2 rounded"
          />
          <button
            onClick={handleAddAddress}
            className="bg-primary text-white py-2 px-4 rounded"
          >
            Add Address
          </button>
        </div>
      </div>
    </div>
  );
}
