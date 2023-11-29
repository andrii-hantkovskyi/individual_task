'use client'

import React, { useEffect } from 'react'
import { useActions } from '@/hooks/useActions'
import { getTokens } from '@/utils/localStorage'

const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const { verify } = useActions()

  useEffect(() => {
    verify(getTokens())
  }, [])


  return children
}

export default AuthProvider