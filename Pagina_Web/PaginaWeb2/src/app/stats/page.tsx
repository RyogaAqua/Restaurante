'use client';

import { useEffect, useState } from 'react';
import { getUserStats } from '@/utils/api';

export default function UserStatsPage() {
  const [stats, setStats] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadStats() {
      try {
        const userId = localStorage.getItem('userId'); // Asegúrate de guardar el ID del usuario al iniciar sesión
        if (!userId) {
          setError('User not logged in');
          return;
        }

        const data = await getUserStats(Number(userId));
        setStats(data.stats);
      } catch (err: any) {
        setError(err.message);
      }
    }

    loadStats();
  }, []);

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!stats) {
    return <div>Loading...</div>;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-8">Your Statistics</h1>
      <div className="space-y-4">
        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="text-xl font-bold">Total Spent</h2>
          <p>${stats.total_spent.toFixed(2)}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="text-xl font-bold">Total Points Earned</h2>
          <p>{stats.total_points_earned}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="text-xl font-bold">Total Orders</h2>
          <p>{stats.total_orders}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="text-xl font-bold">Current Points</h2>
          <p>{stats.current_points}</p>
        </div>
      </div>
    </div>
  );
}
