const baseURL = `${process.env.API_URL}/products`

export const ProductService = {
  async getAll() {
    const res = await fetch(`${baseURL}/`, {
      next: { revalidate: 60 }
    })
    return await res.json()
  }
}