'use client';

import { useState } from 'react';
import { forgotPassword } from '@/utils/api';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await forgotPassword(email);
      setMessage('Password reset email sent successfully!');
      setError(null);
    } catch (err: any) {
      setError(err.message);
      setMessage(null);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-8">Forgot Password</h1>
      {message && <div className="text-green-500">{message}</div>}
      {error && <div className="text-red-500">{error}</div>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="bg-primary text-white py-2 px-4 rounded">
          Send Reset Link
        </button>
      </form>
    </div>
  );
}
