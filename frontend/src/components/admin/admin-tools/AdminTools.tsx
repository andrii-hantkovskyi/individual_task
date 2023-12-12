'use client'

import React, { useState } from 'react'
import styles from './AdminTools.module.scss'
import { adminToolsApi } from '@/store/api/admin.tools.api'
import Modal from '@/components/ui/modal/Modal'
import SignUp from '@/components/auth/sign-up/SignUp'

const AdminTools = () => {
  const [restoreDBDate, setRestoreDBDate] = useState<string>('')
  const { data } = adminToolsApi.useGetAllDBBackupsQuery()
  const [backupDB] = adminToolsApi.useBackupDBMutation()
  const [restoreDB] = adminToolsApi.useRestoreDBMutation()

  const [userCreteModalOpen, setUserCreateModalOpen] = useState<boolean>(false)

  return (
    <div className={styles.adminTools}>
      <Modal isOpen={userCreteModalOpen} onClose={() => setUserCreateModalOpen(false)}><SignUp /></Modal>
      <button onClick={() => setUserCreateModalOpen(true)}>Create user</button>
      <div className={styles.db}>
        <button onClick={() => backupDB()}>Backup db</button>
        <select
          placeholder='Backup date'
          value={restoreDBDate}
          onChange={e => setRestoreDBDate(e.target.value)}
        >
          {
            data &&
            data.map((restoreDate, index) =>
              <option key={index} value={restoreDate}>{restoreDate}</option>)
          }
        </select>
        <button onClick={() => restoreDB(restoreDBDate)}>Restore db</button>
      </div>
    </div>
  )
}

export default AdminTools