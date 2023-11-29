'use client'

import React, { ChangeEvent, useState } from 'react'
import { IUserRegister } from '@/interfaces/user.interface'
import { useActions } from '@/hooks/useActions'
import { useRouter } from 'next/navigation'
import styles from './SignUp.module.scss'

const SignUp = () => {
  const [userData, setUserData] = useState<IUserRegister>({
    email: '',
    phone_number: 380980000000,
    delivery_address: '',
    date_of_birth: '',
    first_name: '',
    middle_name: '',
    last_name: '',
    password: ''
  })
  const {
    email,
    delivery_address,
    phone_number,
    date_of_birth,
    last_name,
    middle_name,
    first_name,
    password
  } = userData

  const { register } = useActions()
  const { push } = useRouter()

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setUserData({ ...userData, [e.target.name]: e.target.value })
  }

  const handleClick = () => {
    register(userData)
    push('/login')
  }

  return (
    <div className={styles.signup}>
      <div>
        <input type='text' name='email' placeholder='Email' value={email} onChange={e => handleChange(e)}
               className='text-4xl' />
        <div className='flex'>
          <input type='text' name='first_name' value={first_name} onChange={e => handleChange(e)}
                 placeholder='First name' />
          <input type='text' name='middle_name' value={middle_name} onChange={e => handleChange(e)}
                 placeholder='Middle name' />
          <input type='text' name='last_name' value={last_name} onChange={e => handleChange(e)}
                 placeholder='Last name' />
        </div>
        <input type='text' name='delivery_address' value={delivery_address} onChange={e => handleChange(e)}
               placeholder='Delivery address' />
        <input type='date' name='date_of_birth' value={date_of_birth} onChange={e => handleChange(e)}
               placeholder='Date of birth' />
        <input type='tel' name='phone_number' value={phone_number} onChange={e => handleChange(e)}
               placeholder='Phone number' />
        <input type='password' name='password' value={password} onChange={e => handleChange(e)}
               placeholder='Password' />
      </div>
      <button
        className='bg-green-400 text-lg rounded-lg px-2 py-1 transition hover:bg-transparent hover:text-green-400'
        onClick={() => handleClick()}
      >
        Register
      </button>
    </div>
  )
}

export default SignUp