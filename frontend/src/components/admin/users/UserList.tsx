import React from 'react'
import { IUsersInfoAdmins } from '@/interfaces/user.interface'
import { isIUserInfoAdmin } from '@/utils/typing'
import UserItemAdmin from '@/components/admin/users/UserItemAdmin'
import UserItemAdvanced from '@/components/admin/users/UserItemAdvanced'

const UserList = ({ users }: { users: IUsersInfoAdmins }) => {
  return (
    <div>
      {
        users.map((user, index) =>
          !isIUserInfoAdmin(user)
            ? <UserItemAdvanced key={index} user={user} />
            : <UserItemAdmin key={user._id} user={user} />
        )
      }
    </div>
  )
}

export default UserList