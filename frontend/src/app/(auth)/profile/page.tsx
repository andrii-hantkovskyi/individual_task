'use client'

import React from 'react'
import { withRoles } from '@/components/hocs/withRoles'
import ProfileInfo from '@/components/users/profile/profile-info/ProfileInfo'
import { useAuth } from '@/hooks/useAuth'

const ProfilePage = () => {
  const { user, isLoading } = useAuth()
  return (
    isLoading ? <h1>Loading...</h1> : user && <ProfileInfo user={user} />
  )
}

export default withRoles(ProfilePage, 'any')