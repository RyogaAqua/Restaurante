'use client';

import { useEffect, useState } from 'react';
import { getNotifications } from '@/utils/api';

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadNotifications() {
      try {
        const userId = localStorage.getItem('userId'); // Asegúrate de guardar el ID del usuario al iniciar sesión
        if (!userId) {
          setError('User not logged in');
          return;
        }

        const data = await getNotifications(Number(userId));
        setNotifications(data.notifications);
      } catch (err: any) {
        setError(err.message);
      }
    }

    loadNotifications();
  }, []);

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-8">Notifications</h1>
      {notifications.length === 0 ? (
        <p>No notifications found.</p>
      ) : (
        <ul className="space-y-4">
          {notifications.map((notification) => (
            <li
              key={notification.id_notification}
              className={`p-4 rounded shadow ${
                notification.type === 'success'
                  ? 'bg-green-100 text-green-800'
                  : notification.type === 'error'
                  ? 'bg-red-100 text-red-800'
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              <p>{notification.message}</p>
              <small>{notification.created_at}</small>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
