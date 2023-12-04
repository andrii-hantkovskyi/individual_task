'use client'

import React from 'react'
import { withRoles } from '@/components/hocs/withRoles'
import { adminUsersApi } from '@/store/api/admin.users.api'
import UserList from '@/components/admin/users/UserList'
import { useAuth } from '@/hooks/useAuth'
import { IUser } from '@/interfaces/user.interface'
import AdminTools from '@/components/admin/admin-tools/AdminTools'
import AdvancedTools from '@/components/admin/advanced-tools/AdvancedTools'

const AdminPage = () => {
  const { data, isLoading } = adminUsersApi.useGetAllUsersQuery()
  const { user } = useAuth()
  const { role } = user as IUser

  if (isLoading) return <div>Loading...</div>

  return (
    <div className='admin-page'>
      {role == 'admin' ? <AdminTools /> : <AdvancedTools />}
      <h1 className='text-5xl mt-8'>Users</h1>
      {data && <UserList users={data} />}
    </div>
  )
}

export default withRoles(AdminPage, ['admin', 'advanced'])