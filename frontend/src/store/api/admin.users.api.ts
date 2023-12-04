import { createApi } from '@reduxjs/toolkit/query/react'
import { fetchBaseQuery } from '@reduxjs/toolkit/dist/query/react'
import { getAccessToken } from '@/utils/localStorage'
import { IUsersInfoAdmins } from '@/interfaces/user.interface'

export const adminUsersApi = createApi({
  reducerPath: 'api/adminUser',
  tagTypes: ['adminUsers'],
  baseQuery: fetchBaseQuery({
    baseUrl: `${process.env['API_URL']}/users`,
    prepareHeaders: (headers, { getState }) => {
      const token = getAccessToken()
      if (token)
        headers.set('Authorization', `Bearer ${token}`)
      return headers
    }
  }),
  endpoints: build => ({
    getAllUsers: build.query<IUsersInfoAdmins, void>({
      query: () => '/get-users',
      providesTags: ['adminUsers']
    }),
    deleteUser: build.mutation<void, string>({
      query: arg => ({
        url: `/delete/${arg}`,
        method: 'DELETE'
      }),
      invalidatesTags: ['adminUsers']
    })
  })
})