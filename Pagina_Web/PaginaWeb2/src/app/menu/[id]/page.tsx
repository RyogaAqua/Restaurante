import Image from 'next/image'

export default function ProductDetails({ params }: { params: { id: string } }) {
  // In a real app, you would fetch the product data based on the ID
  const product = {
    name: 'Burger Smokehouse',
    price: 14.99,
    description: 'Delicious smoked beef patty with crispy bacon, caramelized onions, fresh lettuce, and our special sauce, all served in a toasted brioche bun.',
    image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd',
    rating: 4.5,
    reviews: 128
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-16">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Product Image */}
        <div className="relative h-[400px]">
          <Image
            src={product.image}
            alt={product.name}
            fill
            className="object-cover rounded-lg"
          />
        </div>

        {/* Product Info */}
        <div>
          <h1 className="text-3xl font-bold mb-4">{product.name}</h1>
          <div className="flex items-center gap-2 mb-4">
            <div className="flex text-yellow-400">
              {'★'.repeat(Math.floor(product.rating))}
              {'☆'.repeat(5 - Math.floor(product.rating))}
            </div>
            <span className="text-gray-600">({product.reviews} reviews)</span>
          </div>
          <p className="text-2xl font-bold text-primary mb-6">${product.price}</p>
          <p className="text-gray-600 mb-8">{product.description}</p>
          
          {/* Add to Cart Section */}
          <div className="flex gap-4 items-center">
            <div className="flex items-center border rounded-lg">
              <button className="px-4 py-2 hover:bg-gray-100">-</button>
              <span className="px-4 py-2">1</span>
              <button className="px-4 py-2 hover:bg-gray-100">+</button>
            </div>
            <button className="flex-1 bg-primary hover:bg-primary/90 text-white font-bold py-3 px-8 rounded-lg">
              Add to Cart
            </button>
          </div>

          {/* Additional Info */}
          <div className="mt-8 pt-8 border-t">
            <h3 className="font-bold mb-2">Tags:</h3>
            <div className="flex gap-2">
              <span className="px-3 py-1 bg-gray-100 rounded-full text-sm">Burger</span>
              <span className="px-3 py-1 bg-gray-100 rounded-full text-sm">Beef</span>
              <span className="px-3 py-1 bg-gray-100 rounded-full text-sm">Smokehouse</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
