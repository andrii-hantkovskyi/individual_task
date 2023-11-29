'use client'

import React from 'react'
import { withRoles } from '@/components/hocs/withRoles'
import { orderApi } from '@/store/api/order.api'
import OrderItem from '@/components/orders/OrderItem'
import { useRouter } from 'next/navigation'
import OrderInfo from '@/components/orders/order-info/OrderInfo'

const OrderPage = ({ params }: { params: { id: string } }) => {
  const { data, isLoading } = orderApi.useGetOrderByIdQuery(params.id)
  const { back } = useRouter()

  if (isLoading) return <h1>Loading...</h1>

  return (
    <>
      {
        data ?
          <OrderInfo order={data} />
          : back()
      }
    </>
  )
}

export default withRoles(OrderPage, 'any')