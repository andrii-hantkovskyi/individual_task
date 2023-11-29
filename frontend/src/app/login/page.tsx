'use client'

import React from 'react'
import Login from '@/components/auth/login/Login'
import { useRouter } from 'next/navigation'

const LoginPage = () => {
  const { back } = useRouter()
  return (
    <div>
      <Login back={back} />
    </div>
  )
}

export default LoginPage