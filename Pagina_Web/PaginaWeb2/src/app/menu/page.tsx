import { useEffect, useState } from 'react';
import { fetchMenu } from '@/utils/api';

export default function MenuPage() {
  const [menu, setMenu] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadMenu() {
      try {
        const data = await fetchMenu();
        setMenu(data.menu);
      } catch (err) {
        setError('Failed to load menu');
      }
    }
    loadMenu();
  }, []);

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-8">Menu</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {menu.map((item) => (
          <div key={item.id_objeto} className="bg-white rounded-lg shadow p-4">
            <img src={item.imagen_url} alt={item.nombre_objeto} className="w-full h-48 object-cover rounded" />
            <h2 className="text-xl font-bold mt-4">{item.nombre_objeto}</h2>
            <p className="text-gray-600">${item.precio}</p>
            <button className="mt-4 bg-primary text-white py-2 px-4 rounded">Add to Cart</button>
          </div>
        ))}
      </div>
    </div>
  );
}
