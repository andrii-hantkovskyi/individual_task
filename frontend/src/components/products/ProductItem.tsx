import React, { FC } from 'react'
import { IProductData } from '@/interfaces/product.interface'
import styles from './Products.module.scss'

const ProductItem: FC<IProductData> = ({ product }) => {
  return (
    <div className={styles.productItem}>
      <div>
        <h1>{product.name}</h1>
        <p>{product.type}</p>
      </div>
      <button>Add</button>
    </div>
  )
}

export default ProductItem