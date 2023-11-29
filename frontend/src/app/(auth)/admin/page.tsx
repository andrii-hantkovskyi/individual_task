'use client'

import React from 'react'
import { withRoles } from '@/components/hocs/withRoles'
import { adminUserApi } from '@/store/api/admin.user.api'
import UserList from '@/components/admin/users/UserList'

const AdminPage = () => {
  const { data, isLoading } = adminUserApi.useGetAllUsersQuery()

  if (isLoading) return <div>Loading...</div>

  return (
    <div>
      {data && <UserList users={data} />}
    </div>
  )
}

export default withRoles(AdminPage, ['admin', 'advanced'])