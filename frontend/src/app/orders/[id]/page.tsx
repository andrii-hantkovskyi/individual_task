import React from 'react'

const OrderPage = ({ params }: { params: { id: number } }) => {
  return (
    <div>
      Order {params.id}
    </div>
  )
}

export default OrderPage