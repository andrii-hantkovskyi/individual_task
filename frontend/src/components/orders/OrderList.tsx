import React from 'react'
import { IOrder } from '@/interfaces/order.interface'
import OrderItem from '@/components/orders/OrderItem'

const OrderList = ({ orders }: { orders: IOrder[] }) => {
  return (
    <div>
      {orders && orders.map(order => <OrderItem order={order} key={order._id} />)}
    </div>
  )
}

export default OrderList