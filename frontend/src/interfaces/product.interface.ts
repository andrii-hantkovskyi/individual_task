export interface IProduct {
  _id: string
  type: string
  name: string
}

export interface IProductData {
  product: IProduct
}

export interface IProductsData {
  products: IProduct[]
}