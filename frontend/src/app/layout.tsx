import { Roboto } from 'next/font/google'
import './globals.scss'
import React from 'react'
import Header from '@/components/layout/header/Header'
import StoreProvider from '@/components/providers/StoreProvider'
import AuthProvider from '@/components/providers/AuthProvider'

const roboto = Roboto({ subsets: ['latin'], weight: '400' })

export default function RootLayout({ children }: { children: React.ReactNode }) {

  return (
    <StoreProvider>
      <AuthProvider>
        <html lang='en'>
        <body className={roboto.className}>
        <Header />
        {children}
        </body>
        </html>
      </AuthProvider>
    </StoreProvider>
  )
}
