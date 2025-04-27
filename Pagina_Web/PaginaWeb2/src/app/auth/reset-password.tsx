'use client';

import { useState } from 'react';
import { resetPassword } from '@/utils/api';
import { useSearchParams } from 'next/navigation';

export default function ResetPasswordPage() {
  const [newPassword, setNewPassword] = useState('');
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const searchParams = useSearchParams();
  const token = searchParams.get('token');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newPassword || newPassword.length < 6) {
      setError('Password must be at least 6 characters long.');
      setMessage(null);
      return;
    }
    try {
      if (!token) {
        throw new Error('Invalid or missing token.');
      }
      await resetPassword(token, newPassword);
      setMessage('Password reset successfully!');
      setError(null);
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred.');
      setMessage(null);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-8">Reset Password</h1>
      {message && <div className="text-green-500">{message}</div>}
      {error && <div className="text-red-500">{error}</div>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="newPassword" className="block text-sm font-medium text-gray-700">
            New Password
          </label>
          <input
            type="password"
            id="newPassword"
            name="newPassword"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary sm:text-sm"
          />
        </div>
        <button
          type="submit"
          className="bg-primary text-white py-2 px-4 rounded hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        >
          Reset Password
        </button>
      </form>
    </div>
  );
}
