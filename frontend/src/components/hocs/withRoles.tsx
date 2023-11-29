'use client'

import { useRouter } from 'next/navigation'
import { TRole } from '@/interfaces/user.interface'
import { useAuth } from '@/hooks/useAuth'
import { useEffect, useState } from 'react'

type TRoles = TRole[] | 'any'

const hasRequiredRole = (requiredRoles: TRoles, userRole: TRole): boolean =>
  requiredRoles === 'any' || requiredRoles.includes(userRole)


export function withRoles(Component: any, requiredRoles: TRoles) {
  return function WithRolesWrapper(props: any) {
    const { user } = useAuth()
    const { replace } = useRouter()

    const [hasPermission, setHasPermission] = useState<boolean | null>(null)

    useEffect(() => {
      if (user) {
        const permission = hasRequiredRole(requiredRoles, user.role)
        setHasPermission(permission)

        if (!permission) {
          replace('/')
        }
      } else {
        replace('/')
      }
    }, [replace, user])


    if (hasPermission) {
      return <Component {...props} />
    } else {
      return null
    }
  }
}