'use client'

import React, { ChangeEvent, useEffect, useState } from 'react'
import { ILoginData } from '@/interfaces/user.interface'
import { useActions } from '@/hooks/useActions'
import { useAuth } from '@/hooks/useAuth'
import { useRouter } from 'next/navigation'


const Login = () => {
  const [loginData, setLoginData] = useState<ILoginData>({
    email: '',
    password: ''
  })
  const { email, password } = loginData

  const { login } = useActions()
  const { isAuthenticated } = useAuth()

  const { replace } = useRouter()

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setLoginData({ ...loginData, [e.target.name]: e.target.value })
  }

  const handleClick = () => {
    if (!email || !password) return
    login(loginData)
  }

  useEffect(() => {
    if (isAuthenticated) replace('/')
  }, [isAuthenticated])

  return (
    <div className='flex flex-col items-center justify-between h-56'>
      <div className='flex flex-col justify-between h-32'>
        <input type='email'
               className='border-2 border-pink-500 text-white bg-transparent text-2xl rounded-lg p-2'
               name='email'
               value={email}
               onChange={e => handleChange(e)}
        />
        <input type='password'
               className='border-2 border-pink-500 text-white bg-transparent text-2xl rounded-lg p-2'
               name='password'
               value={password}
               onChange={e => handleChange(e)}
        />
      </div>
      <button
        className='border-2 transition border-cyan-500 hover:bg-cyan-500 text-white bg-transparent text-2xl rounded-lg px-4 py-2'
        onClick={handleClick}
      >
        Login
      </button>
    </div>
  )
}

export default Login