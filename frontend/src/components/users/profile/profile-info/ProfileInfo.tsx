import React, { ChangeEvent, useState } from 'react'
import { IUser } from '@/interfaces/user.interface'
import styles from './ProfileInfo.module.scss'
import { useActions } from '@/hooks/useActions'

const ProfileInfo = ({ user }: { user: IUser }) => {
  const { updateProfile } = useActions()
  const [userData, setUserData] = useState<IUser>(user)
  const {
    first_name, last_name, middle_name,
    delivery_address, phone_number, date_of_birth
  } = userData

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setUserData({ ...userData, [e.target.name]: e.target.value })
  }

  const handleClick = () => {
    updateProfile(userData)
  }

  return (
    <div className={styles.profileInfo}>
      <div>
        <h1 className='text-4xl'>{userData.email}</h1>
        <h1 className='text-red-500 text-2xl'>{userData.role}</h1>
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
      </div>
      <button onClick={handleClick}>Save</button>
    </div>
  )
}

export default ProfileInfo