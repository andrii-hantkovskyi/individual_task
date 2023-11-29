'use client'

import React from 'react'
import { withRoles } from '@/components/hocs/withRoles'

const AdminPage = () => {
  return (
    <div>
      Admin
    </div>
  )
}

export default withRoles(AdminPage, ['admin', 'advanced'])