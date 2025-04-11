import Image from 'next/image'
import Link from 'next/link'

export default function Home() {
  return (
    <div>
      {/* Hero Section */}
      <div className="relative h-[600px]">
        <Image
          src="https://images.unsplash.com/photo-1513104890138-7c749659a591"
          alt="Delicious burger"
          fill
          className="object-cover brightness-50"
        />
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center text-white">
            <h1 className="text-5xl font-bold mb-4">Welcome to Handout</h1>
            <p className="text-xl mb-8">Discover our delicious menu of burgers and more</p>
            <Link 
              href="/menu" 
              className="bg-primary hover:bg-primary/90 text-white font-bold py-3 px-8 rounded-full"
            >
              Order Now
            </Link>
          </div>
        </div>
      </div>

      {/* Featured Categories */}
      <div className="max-w-7xl mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-center mb-12">Our Categories</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {categories.map((category) => (
            <Link 
              key={category.name}
              href={`/menu/${category.slug}`}
              className="group relative h-64 overflow-hidden rounded-lg"
            >
              <Image
                src={category.image}
                alt={category.name}
                fill
                className="object-cover group-hover:scale-110 transition-transform duration-300"
              />
              <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
                <h3 className="text-white text-2xl font-bold">{category.name}</h3>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}

const categories = [
  {
    name: 'Burgers',
    slug: 'burgers',
    image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd'
  },
  {
    name: 'Pizzas',
    slug: 'pizzas',
    image: 'https://images.unsplash.com/photo-1513104890138-7c749659a591'
  },
  {
    name: 'Drinks',
    slug: 'drinks',
    image: 'https://images.unsplash.com/photo-1544145945-f90425340c7e'
  }
]
