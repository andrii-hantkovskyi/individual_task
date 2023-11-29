import React from 'react'
import { IOrder } from '@/interfaces/order.interface'
import { useRouter } from 'next/navigation'
import { orderApi } from '@/store/api/order.api'

const OrderItem = ({ order }: { order: IOrder }) => {

  const { push } = useRouter()
  const [removeOrder, _] = orderApi.useRemoveOrderMutation()

  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation()
    removeOrder(order._id)
  }

  return (
    <div className='flex justify-between items-center border-2 border-cyan-500 p-3 m-2 rounded-lg'
         onClick={() => push(`orders/${order._id}`)}>
      <div className='flex flex-col mr-4'>
        <span className='text-pink-500'>Name: {order.product.name}</span>
        Qty: {order.qty}
      </div>
      <button
        className='transition border-red-500 border-2 px-1.5 rounded-md text-red-500 hover:bg-red-500 hover:text-white'
        onClick={e => handleClick(e)}>X
      </button>
    </div>
  )
}

export default OrderItem