'use client';

import { useState } from 'react';
import { updateUserProfile } from '@/utils/api';

export default function ProfilePage() {
  const [formData, setFormData] = useState({
    nombre_usuario: '',
    apellido_usuario: '',
    email: '',
    telefono: '',
    address: {
      address: '',
      city: '',
      state: '',
      zip_code: '',
      country: '',
    },
  });
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    if (name in formData.address) {
      setFormData({
        ...formData,
        address: { ...formData.address, [name]: value },
      });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const userId = localStorage.getItem('userId'); // Asegúrate de guardar el ID del usuario al iniciar sesión
      if (!userId) {
        setErrorMessage('User not logged in');
        return;
      }
      const response = await updateUserProfile(Number(userId), formData);
      setSuccessMessage('Profile updated successfully!');
      setErrorMessage(null);
    } catch (error: any) {
      setErrorMessage(error.message);
      setSuccessMessage(null);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-8">Update Profile</h1>
      {successMessage && <div className="text-green-500">{successMessage}</div>}
      {errorMessage && <div className="text-red-500">{errorMessage}</div>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="nombre_usuario">First Name</label>
          <input
            type="text"
            id="nombre_usuario"
            name="nombre_usuario"
            value={formData.nombre_usuario}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="apellido_usuario">Last Name</label>
          <input
            type="text"
            id="apellido_usuario"
            name="apellido_usuario"
            value={formData.apellido_usuario}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="telefono">Phone</label>
          <input
            type="text"
            id="telefono"
            name="telefono"
            value={formData.telefono}
            onChange={handleChange}
          />
        </div>
        <div>
          <label htmlFor="address">Address</label>
          <input
            type="text"
            id="address"
            name="address"
            value={formData.address.address}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="city">City</label>
          <input
            type="text"
            id="city"
            name="city"
            value={formData.address.city}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="state">State</label>
          <input
            type="text"
            id="state"
            name="state"
            value={formData.address.state}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="zip_code">Zip Code</label>
          <input
            type="text"
            id="zip_code"
            name="zip_code"
            value={formData.address.zip_code}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="country">Country</label>
          <input
            type="text"
            id="country"
            name="country"
            value={formData.address.country}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" className="bg-primary text-white py-2 px-4 rounded">
          Update Profile
        </button>
      </form>
    </div>
  );
}
