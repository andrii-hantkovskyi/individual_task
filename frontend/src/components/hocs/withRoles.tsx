'use client'

import { useRouter } from 'next/navigation'
import { IUser, TRole } from '@/interfaces/user.interface'
import { useAuth } from '@/hooks/useAuth'
import { useEffect, useState } from 'react'

type TRoles = TRole[] | 'any'

const hasRequiredRole = (requiredRoles: TRoles, userRole: TRole): boolean =>
  requiredRoles === 'any' || requiredRoles.includes(userRole)


export function withRoles(Component: any, requiredRoles: TRoles) {
  return function WithRolesWrapper(props: any) {
    const { user } = useAuth()
    const { replace } = useRouter()

    const [userData, setUserData] = useState<IUser | null>(null)
    const [hasPermission, setHasPermission] = useState<boolean | null>(null)

    useEffect(() => {
      if (user) setUserData(user)
    }, [user])

    useEffect(() => {
      if (userData) setHasPermission(hasRequiredRole(requiredRoles, userData.role))
    }, [userData])

    // if (hasPermission === null) console.log('loading')

    if (hasPermission) {
      return <Component {...props} />
    } else {
      // replace('/')
      return null
    }
  }
}