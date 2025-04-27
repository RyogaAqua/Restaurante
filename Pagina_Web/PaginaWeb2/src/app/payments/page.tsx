'use client';

import { useEffect, useState } from 'react';
import { getPaymentHistory } from '@/utils/api';

export default function PaymentHistoryPage() {
  const [payments, setPayments] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadPaymentHistory() {
      try {
        const userId = localStorage.getItem('userId'); // Asegúrate de guardar el ID del usuario al iniciar sesión
        if (!userId) {
          setError('User not logged in');
          return;
        }

        const data = await getPaymentHistory(Number(userId));
        setPayments(data.payments);
      } catch (err: any) {
        setError(err.message);
      }
    }

    loadPaymentHistory();
  }, []);

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-8">Payment History</h1>
      {payments.length === 0 ? (
        <p>No payments found.</p>
      ) : (
        <div className="space-y-4">
          {payments.map((payment) => (
            <div key={payment.order_id} className="bg-white rounded-lg shadow p-4">
              <h2 className="text-xl font-bold">Order #{payment.order_id}</h2>
              <p className="text-gray-600">Total: ${payment.total_price.toFixed(2)}</p>
              <p className="text-gray-600">Date: {payment.payment_date}</p>
              <p className="text-gray-600">Points Earned: {payment.points_earned}</p>
              <p className="text-gray-600">Points Spent: {payment.points_spent}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
