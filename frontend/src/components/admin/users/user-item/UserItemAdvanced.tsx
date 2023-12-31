import React from 'react'
import { IUserInfoAdvanced } from '@/interfaces/user.interface'

import styles from './UserItem.module.scss'


const UserItemAdvanced = ({ user }: { user: IUserInfoAdvanced }) => {
  return (
    <div className={styles.userItem}>
      <p>{user.first_name}</p>
      <p>{user.email}</p>
    </div>
  )
}

export default UserItemAdvanced