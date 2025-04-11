import Link from 'next/link'
import { ShoppingCartIcon } from '@heroicons/react/24/outline'

export default function Navbar() {
  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link href="/" className="flex-shrink-0 flex items-center">
              <span className="text-2xl font-bold text-primary">Handout</span>
            </Link>
            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
              <Link href="/menu" className="text-gray-900 hover:text-primary px-3 py-2 rounded-md text-sm font-medium">
                Menu
              </Link>
              <Link href="/gallery" className="text-gray-900 hover:text-primary px-3 py-2 rounded-md text-sm font-medium">
                Gallery
              </Link>
              <Link href="/events" className="text-gray-900 hover:text-primary px-3 py-2 rounded-md text-sm font-medium">
                Events
              </Link>
              <Link href="/blog" className="text-gray-900 hover:text-primary px-3 py-2 rounded-md text-sm font-medium">
                Blog
              </Link>
              <Link href="/contact" className="text-gray-900 hover:text-primary px-3 py-2 rounded-md text-sm font-medium">
                Contact
              </Link>
            </div>
          </div>
          <div className="flex items-center">
            <Link href="/cart" className="p-2 rounded-full hover:bg-gray-100">
              <ShoppingCartIcon className="h-6 w-6 text-gray-900" />
            </Link>
            <Link href="/signin" className="ml-4 px-4 py-2 rounded bg-primary text-white hover:bg-primary/90">
              Sign In
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}
