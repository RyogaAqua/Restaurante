'use client';

import { useEffect, useState } from 'react';
import { sendSupportMessage, getSupportMessages } from '@/utils/api';

export default function SupportPage() {
  const [messages, setMessages] = useState<any[]>([]);
  const [formData, setFormData] = useState({ subject: '', message: '' });
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    async function loadMessages() {
      try {
        const userId = localStorage.getItem('userId'); // Asegúrate de guardar el ID del usuario al iniciar sesión
        if (!userId) {
          setError('User not logged in');
          return;
        }

        const data = await getSupportMessages(Number(userId));
        setMessages(data.messages);
      } catch (err: any) {
        setError(err.message);
      }
    }

    loadMessages();
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    try {
      const userId = localStorage.getItem('userId');
      if (!userId) {
        setError('User not logged in');
        return;
      }

      await sendSupportMessage(Number(userId), formData.subject, formData.message);
      setSuccess('Message sent successfully!');
      setFormData({ subject: '', message: '' });
      setError(null);

      // Reload messages
      const data = await getSupportMessages(Number(userId));
      setMessages(data.messages);
    } catch (err: any) {
      setError(err.message);
      setSuccess(null);
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-8">Support</h1>
      {error && <div className="text-red-500">{error}</div>}
      {success && <div className="text-green-500">{success}</div>}
      <form onSubmit={handleSubmit} className="space-y-4 mb-8">
        <div>
          <label htmlFor="subject">Subject</label>
          <input
            type="text"
            id="subject"
            name="subject"
            value={formData.subject}
            onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
            required
            className="w-full border p-2 rounded"
          />
        </div>
        <div>
          <label htmlFor="message">Message</label>
          <textarea
            id="message"
            name="message"
            value={formData.message}
            onChange={(e) => setFormData({ ...formData, message: e.target.value })}
            required
            className="w-full border p-2 rounded"
          />
        </div>
        <button type="submit" className="bg-primary text-white py-2 px-4 rounded">
          Send Message
        </button>
      </form>
      <h2 className="text-2xl font-bold mb-4">Message History</h2>
      <div className="space-y-4">
        {messages.map((msg) => (
          <div key={msg.id_message} className="bg-white rounded-lg shadow p-4">
            <h3 className="text-xl font-bold">{msg.subject}</h3>
            <p>{msg.message}</p>
            <small className="text-gray-500">{msg.created_at}</small>
          </div>
        ))}
      </div>
    </div>
  );
}
