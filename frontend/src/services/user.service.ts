import { ILoginData, ITokens, IUser, IUserAuth, IUserBase, IUserData } from '@/interfaces/user.interface'
import axios from 'axios'
import { getAccessToken } from '@/utils/localStorage'

axios.defaults.baseURL = `${process.env.API_URL}/users`

export const userService = {
  async register(data: IUserData) {
    await axios.post('/register', data)
  },
  async login(data: ILoginData) {
    return await axios.post<IUserAuth>('/login', data).then(res => res.data)
  },
  async verify({ access_token }: ITokens) {
    return await axios.post<IUser>('/verify', {}, {
      headers: {
        Authorization: `Bearer ${access_token}`
      }
    }).then(res => res.data)
  },
  async refresh({ refresh_token }: ITokens) {
    return await axios.post<IUserAuth>('/refresh', refresh_token).then(res => res.data)
  },
  async updateProfile(updateData: IUserBase) {
    return await axios.put<IUser>('/update-info', updateData, {
      headers: {
        Authorization: `Bearer ${getAccessToken()}`
      }
    }).then(res => res.data)
  }
}