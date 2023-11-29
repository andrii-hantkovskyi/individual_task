import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { IOrder, IOrderCreate } from '@/interfaces/order.interface'
import { getAccessToken } from '@/utils/localStorage'

export const orderApi = createApi({
  reducerPath: 'orderApi',
  tagTypes: ['Orders'],
  baseQuery: fetchBaseQuery({
    baseUrl: `${process.env['API_URL']}/orders`,
    prepareHeaders: (headers, { getState }) => {
      headers.set('Authorization', `Bearer ${getAccessToken()}`)
      return headers
    }
  }),
  endpoints: build => ({
    getAllOrders: build.query<IOrder[], void>({
      query: () => '/',
      providesTags: ['Orders']
    }),
    getOrderById: build.query<IOrder, string>({
      query: arg => `/${arg}`,
      providesTags: ['Orders']
    }),
    createOrder: build.mutation<IOrder, IOrderCreate>({
      query: arg => ({
        url: '/',
        body: arg,
        method: 'POST'
      }),
      invalidatesTags: (_, error) => error ? [] : ['Orders']
    }),
    removeOrder: build.mutation<void, string>({
      query: arg => ({
        url: `/${arg}`,
        method: 'DELETE'
      }),
      invalidatesTags: (_, error) => error ? [] : ['Orders']
    })
  })
})