import React from 'react'
import { IOrder } from '@/interfaces/order.interface'

const OrderInfo = ({ order }: { order: IOrder }) => {
  return (
    <div>
      <h2>{order.product.name} &times; {order.qty}</h2>
    </div>
  )
}

export default OrderInfo