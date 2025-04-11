export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Newsletter Signup */}
          <div className="md:col-span-2">
            <h3 className="text-xl font-bold mb-4">Don&apos;t Miss Our Update</h3>
            <form className="flex gap-2">
              <input
                type="email"
                placeholder="Your Email"
                className="flex-1 px-4 py-2 rounded text-gray-900"
              />
              <button
                type="submit"
                className="bg-red-600 hover:bg-red-700 px-6 py-2 rounded"
              >
                Subscribe Now
              </button>
            </form>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-xl font-bold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li><a href="/about" className="hover:text-primary">About Us</a></li>
              <li><a href="/menu" className="hover:text-primary">Menu</a></li>
              <li><a href="/blog" className="hover:text-primary">Blog</a></li>
              <li><a href="/gallery" className="hover:text-primary">Gallery</a></li>
              <li><a href="/contact" className="hover:text-primary">Contact</a></li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-xl font-bold mb-4">Contact Us</h3>
            <ul className="space-y-2">
              <li>123 Restaurant Street</li>
              <li>City, State 12345</li>
              <li>Phone: (123) 456-7890</li>
              <li>Email: info@handout.com</li>
            </ul>
          </div>
        </div>

        {/* Copyright */}
        <div className="mt-8 pt-8 border-t border-gray-800 text-center">
          <p>Copyright ©2023 Handout. All Rights Reserved by Heart Coding</p>
          <div className="flex justify-center gap-4 mt-4">
            <a href="#" className="hover:text-primary">Facebook</a>
            <a href="#" className="hover:text-primary">Twitter</a>
            <a href="#" className="hover:text-primary">Instagram</a>
            <a href="#" className="hover:text-primary">YouTube</a>
          </div>
        </div>
      </div>
    </footer>
  )
}
