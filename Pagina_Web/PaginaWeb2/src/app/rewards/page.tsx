'use client';

import { useEffect, useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default function RewardsPage() {
  const [rewards, setRewards] = useState<any[]>([]);
  const [userPoints, setUserPoints] = useState<number>(0);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchRewards() {
      try {
        const userId = localStorage.getItem('userId'); // Asegúrate de guardar el ID del usuario al iniciar sesión
        if (!userId) {
          setError('User not logged in');
          return;
        }

        const response = await fetch(`${API_URL}/rewards?user_id=${userId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch rewards');
        }

        const data = await response.json();
        setRewards(data.rewards);

        // Simula obtener los puntos del usuario
        const pointsResponse = await fetch(`${API_URL}/user/${userId}/points`);
        if (!pointsResponse.ok) {
          throw new Error('Failed to fetch user points');
        }

        const pointsData = await pointsResponse.json();
        setUserPoints(pointsData.points);
      } catch (err: any) {
        setError(err.message);
      }
    }

    fetchRewards();
  }, []);

  async function redeemReward(rewardName: string) {
    try {
      const userId = localStorage.getItem('userId');
      if (!userId) {
        setError('User not logged in');
        return;
      }

      const response = await fetch(`${API_URL}/rewards/redeem`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: userId, reward_name: rewardName }),
      });

      if (!response.ok) {
        throw new Error('Failed to redeem reward');
      }

      const data = await response.json();
      alert(data.message);

      // Actualiza las recompensas y puntos después de canjear
      setRewards((prevRewards) =>
        prevRewards.filter((reward) => reward.reward !== rewardName)
      );
      setUserPoints((prevPoints) => prevPoints - data.required_points);
    } catch (err: any) {
      setError(err.message);
    }
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-8">Your Rewards</h1>
      <p className="mb-4">You have <strong>{userPoints}</strong> points.</p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {rewards.map((reward) => (
          <div key={reward.reward} className="bg-white rounded-lg shadow p-4">
            <h2 className="text-xl font-bold">{reward.reward}</h2>
            <p className="text-gray-600">Requires {reward.required_points} points</p>
            <button
              className="mt-4 bg-primary text-white py-2 px-4 rounded"
              onClick={() => redeemReward(reward.reward)}
            >
              Redeem
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
