export interface IOrder {
  _id: number
  product_id: number
  qty: number
}

export interface IOrderData {
  order: IOrder
}

export interface IOrdersData {
  orders: IOrder[]
}
