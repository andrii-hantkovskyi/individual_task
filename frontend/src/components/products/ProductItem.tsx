'use client'

import React, { FC } from 'react'
import { IProductData } from '@/interfaces/product.interface'
import styles from './Products.module.scss'
import { orderApi } from '@/store/api/order.api'


const ProductItem: FC<IProductData> = ({ product }) => {
  const [createOrder, { isLoading }] = orderApi.useCreateOrderMutation()

  return (
    <div className={styles.productItem}>
      <div>
        <h1>{product.name}</h1>
        <p>{product.type}</p>
      </div>
      <button onClick={() => createOrder({ product_id: product._id, qty: 1 })}>Add</button>
    </div>
  )
}

export default ProductItem