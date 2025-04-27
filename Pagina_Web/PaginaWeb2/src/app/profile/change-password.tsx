'use client';

import { useState } from 'react';
import { changePassword } from '@/utils/api';

export default function ChangePasswordPage() {
  const [formData, setFormData] = useState({
    currentPassword: '',
    newPassword: '',
  });
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const userId = localStorage.getItem('userId'); // Asegúrate de guardar el ID del usuario al iniciar sesión
      if (!userId) {
        setErrorMessage('User not logged in');
        return;
      }
      await changePassword(Number(userId), formData.currentPassword, formData.newPassword);
      setSuccessMessage('Password changed successfully!');
      setErrorMessage(null);
      setFormData({ currentPassword: '', newPassword: '' });
    } catch (error: any) {
      setErrorMessage(error.message);
      setSuccessMessage(null);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-8">Change Password</h1>
      {successMessage && <div className="text-green-500">{successMessage}</div>}
      {errorMessage && <div className="text-red-500">{errorMessage}</div>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="currentPassword">Current Password</label>
          <input
            type="password"
            id="currentPassword"
            name="currentPassword"
            value={formData.currentPassword}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="newPassword">New Password</label>
          <input
            type="password"
            id="newPassword"
            name="newPassword"
            value={formData.newPassword}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" className="bg-primary text-white py-2 px-4 rounded">
          Change Password
        </button>
      </form>
    </div>
  );
}
