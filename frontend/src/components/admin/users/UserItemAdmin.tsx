import React from 'react'
import { IUserInfoAdmin } from '@/interfaces/user.interface'
import { adminUserApi } from '@/store/api/admin.user.api'

const UserItemAdmin = ({ user }: { user: IUserInfoAdmin }) => {
  const [deleteUser, _] = adminUserApi.useDeleteUserMutation()

  return (
    <div>
      <p>{user._id}</p>
      <p>{user.role}</p>
      <p>{user.first_name}</p>
      <p>{user.middle_name}</p>
      <p>{user.last_name}</p>
      <p>{user.email}</p>
      <p>{user.date_of_birth}</p>
      <p>{user.delivery_address}</p>
      <p>{user.phone_number}</p>
      <button
        className='bg-red-500 rounded-lg px-2 py-1 text-2-xl hover:bg-transparent hover:text-red-500 transition'
        onClick={() => deleteUser(user._id)}
      >
        Delete
      </button>
    </div>
  )
}

export default UserItemAdmin