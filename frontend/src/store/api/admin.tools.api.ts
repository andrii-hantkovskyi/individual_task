import { createApi } from '@reduxjs/toolkit/query/react'
import { fetchBaseQuery } from '@reduxjs/toolkit/dist/query/react'
import { getAccessToken } from '@/utils/localStorage'

export const adminToolsApi = createApi({
  reducerPath: 'api/adminTool',
  tagTypes: ['dbBackups'],
  baseQuery: fetchBaseQuery({
    baseUrl: `${process.env['API_URL']}/admin/`,
    prepareHeaders: (headers, { getState }) => {
      const token = getAccessToken()
      if (token)
        headers.set('Authorization', `Bearer ${token}`)
      return headers
    }
  }),
  endpoints: build => ({
    getAllDBBackups: build.query<string[], void>({
      query: () => '/db-backups',
      providesTags: ['dbBackups']
    }),
    backupDB: build.mutation<void, void>({
      query: () => ({
        url: '/backup-db',
        method: 'POST'
      }),
      invalidatesTags: ['dbBackups']
    }),
    restoreDB: build.mutation<void, string>({
      query: arg => ({
        url: `/restore-db`,
        method: 'POST',
        body: { date: arg }
      })
    })
  })
})