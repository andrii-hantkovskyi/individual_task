import React, { FC } from 'react'
import { IProductsData } from '@/interfaces/product.interface'
import ProductItem from '@/components/products/ProductItem'
import styles from './Products.module.scss'

const ProductList: FC<IProductsData> = ({ products }) => {
  return (
    <div className={styles.productList}>
      {products.length && products.map(product => (
        <ProductItem key={product._id} product={product} />
      ))}
    </div>
  )
}

export default ProductList