import React from 'react'
import { IUserInfoAdvanced } from '@/interfaces/user.interface'

const UserItemAdvanced = ({ user }: { user: IUserInfoAdvanced }) => {
  return (
    <div>
      <p>{user.first_name}</p>
      <p>{user.email}</p>
    </div>
  )
}

export default UserItemAdvanced