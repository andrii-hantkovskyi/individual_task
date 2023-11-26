import React from 'react'
import ProductList from '@/components/products/ProductList'
import { ProductService } from '@/services/product.service'
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Products',
  description: 'products'
}

export default async function ProductsPage() {
  const products = await ProductService.getAll()
  return (
    <ProductList products={products} />
  )
}
