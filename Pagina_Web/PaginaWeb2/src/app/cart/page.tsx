import Image from 'next/image'
import Link from 'next/link'

export default function Cart() {
  // In a real app, this would come from your cart state management
  const cartItems = [
    {
      id: 1,
      name: 'Burger Bistro',
      price: 14.99,
      quantity: 2,
      image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd'
    },
    {
      id: 2,
      name: 'Hot Cross Buns',
      price: 9.99,
      quantity: 1,
      image: 'https://images.unsplash.com/photo-1587593810167-a84920ea0781'
    }
  ]

  const subtotal = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0)
  const shipping = 5.00
  const total = subtotal + shipping

  return (
    <div className="max-w-7xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-8">Shopping Cart</h1>

      {/* Cart Items */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow">
            <table className="w-full">
              <thead className="border-b">
                <tr>
                  <th className="px-6 py-3 text-left">Product</th>
                  <th className="px-6 py-3 text-center">Quantity</th>
                  <th className="px-6 py-3 text-right">Total</th>
                </tr>
              </thead>
              <tbody>
                {cartItems.map((item) => (
                  <tr key={item.id} className="border-b">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-4">
                        <div className="relative w-16 h-16">
                          <Image
                            src={item.image}
                            alt={item.name}
                            fill
                            className="object-cover rounded"
                          />
                        </div>
                        <div>
                          <h3 className="font-medium">{item.name}</h3>
                          <p className="text-gray-600">${item.price}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex justify-center items-center gap-2">
                        <button className="p-1 hover:bg-gray-100 rounded">-</button>
                        <span>{item.quantity}</span>
                        <button className="p-1 hover:bg-gray-100 rounded">+</button>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      ${(item.price * item.quantity).toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Order Summary */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4">Cart Totals</h2>
          <div className="space-y-4">
            <div className="flex justify-between">
              <span>Subtotal</span>
              <span>${subtotal.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span>Shipping</span>
              <span>${shipping.toFixed(2)}</span>
            </div>
            <div className="flex justify-between font-bold text-lg pt-4 border-t">
              <span>Total</span>
              <span>${total.toFixed(2)}</span>
            </div>
            <button className="w-full bg-primary hover:bg-primary/90 text-white font-bold py-3 px-4 rounded">
              Proceed to Checkout
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
