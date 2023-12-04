'use client'

import React, { useState } from 'react'
import styles from './AdminTools.module.scss'
import { adminToolsApi } from '@/store/api/admin.tools.api'

const AdminTools = () => {
  const [restoreDBDate, setRestoreDBDate] = useState<string>('')
  const { data } = adminToolsApi.useGetAllDBBackupsQuery()
  const [backupDB] = adminToolsApi.useBackupDBMutation()
  const [restoreDB] = adminToolsApi.useRestoreDBMutation()

  return (
    <div className={styles.adminTools}>
      <button>Create user</button>
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