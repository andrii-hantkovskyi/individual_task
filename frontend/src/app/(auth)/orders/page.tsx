'use client'

import React from 'react'
import { NextPage } from 'next'
import { withRoles } from '@/components/hocs/withRoles'
import { orderApi } from '@/store/api/order.api'
import OrderList from '@/components/orders/OrderList'

const OrdersPage: NextPage = () => {
  const { data, isLoading } = orderApi.useGetAllOrdersQuery()

  if (isLoading) return <h1>Loading...</h1>

  return (
    <>
      {
        data ?
          <OrderList orders={data} />
          : <h1>No orders</h1>
      }
    </>
  )
}

export default withRoles(OrdersPage, 'any')