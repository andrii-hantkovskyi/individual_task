'use client'

import React, { Fragment } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

const navLinks = [
  { href: '/', text: 'Home' },
  { href: '/products', text: 'Products' },
  { href: '/orders', text: 'Orders', isOnlyAuth: true },
  { href: '/profile', text: 'Profile', isOnlyAuth: true }
]

const authLinks = [
  { href: '/sign-up', 'text': 'Sign Up' },
  { href: '/login', 'text': 'Login' }
]

const isLoggedIn = false

const Header = () => {
  const pathname = usePathname()
  return (
    <header className='fixed top-0 w-full'>
      <div className='mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between'>
        <div>
          <h1 className='font-bold text-3xl'>Ind task</h1>
          <nav className='mt-4'>
            <ul className='flex space-x-4'>
              {navLinks.map(
                (navLink, index) =>
                  navLink.isOnlyAuth && !isLoggedIn ? <Fragment key={index} /> :
                    <li key={index}>
                      <Link
                        href={navLink.href}
                        className={`hover:text-cyan-200 transition ${pathname === navLink.href ? 'text-white' : 'text-cyan-400'}`}
                      >
                        {navLink.text}
                      </Link>
                    </li>
              )}
            </ul>
          </nav>
        </div>
        {
          !isLoggedIn
          &&
          <div className='flex items-end justify-between w-28'>
            {
              authLinks.map((authLink, index) =>
                <Link
                  key={index}
                  className={`hover:text-cyan-200 transition ${pathname === authLink.href ? 'text-white' : 'text-cyan-400'}`}
                  href={authLink.href}
                >
                  {authLink.text}
                </Link>
              )
            }
          </div>
        }
      </div>
    </header>
  )
}

export default Header