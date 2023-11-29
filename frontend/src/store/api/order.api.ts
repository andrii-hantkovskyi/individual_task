import { createApi } from '@reduxjs/toolkit/query/react'

const ordersApi = createApi({
  reducerPath: 'api/orders',
  baseQuery: args => {

  }
})