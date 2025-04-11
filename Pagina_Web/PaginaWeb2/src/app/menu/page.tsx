import Image from 'next/image'
import Link from 'next/link'

export default function Menu() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-16">
      <h1 className="text-4xl font-bold text-center mb-12">Our Menu</h1>
      
      {/* Category Filters */}
      <div className="flex justify-center gap-4 mb-12">
        {categories.map((category) => (
          <button
            key={category.id}
            className="flex flex-col items-center p-4 rounded-lg hover:bg-gray-100"
          >
            <div className="w-12 h-12 relative mb-2">
              <Image
                src={category.icon}
                alt={category.name}
                fill
                className="object-contain"
              />
            </div>
            <span className="text-sm font-medium">{category.name}</span>
          </button>
        ))}
      </div>

      {/* Menu Items Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {menuItems.map((item) => (
          <Link
            key={item.id}
            href={`/menu/${item.id}`}
            className="flex gap-4 p-4 rounded-lg hover:bg-gray-50"
          >
            <div className="relative w-24 h-24">
              <Image
                src={item.image}
                alt={item.name}
                fill
                className="object-cover rounded-lg"
              />
            </div>
            <div className="flex-1">
              <div className="flex justify-between items-start">
                <h3 className="text-lg font-semibold">{item.name}</h3>
                <span className="text-primary font-bold">${item.price}</span>
              </div>
              <p className="text-gray-600 text-sm mt-1">{item.description}</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}

const categories = [
  { id: 1, name: 'Burgers', icon: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd' },
  { id: 2, name: 'Chicken', icon: 'https://images.unsplash.com/photo-1587593810167-a84920ea0781' },
  { id: 3, name: 'Beverage', icon: 'https://images.unsplash.com/photo-1544145945-f90425340c7e' },
  { id: 4, name: 'Coffee', icon: 'https://images.unsplash.com/photo-1509042239860-f550ce710b93' },
  { id: 5, name: 'Pizza', icon: 'https://images.unsplash.com/photo-1513104890138-7c749659a591' }
]

const menuItems = [
  {
    id: 1,
    name: 'Classic Burger',
    description: 'Fresh beef patty with lettuce, tomato, and special sauce',
    price: 12.99,
    image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd'
  },
  {
    id: 2,
    name: 'Chicken Wings',
    description: '8 pieces of crispy wings with your choice of sauce',
    price: 14.99,
    image: 'https://images.unsplash.com/photo-1587593810167-a84920ea0781'
  },
  // Add more menu items as needed
]
