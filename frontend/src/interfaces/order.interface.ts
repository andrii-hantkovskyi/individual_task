import { IProduct } from '@/interfaces/product.interface'

export interface IOrderCreate {
  product_id: string
  qty: number
}

export interface IOrder {
  _id: string
  product: IProduct
  qty: number
}

export interface IOrderData {
  order: IOrder
}

export interface IOrdersData {
  orders: IOrder[]
}
