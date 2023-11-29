import { IUser } from '@/interfaces/user.interface'

export interface IAuthInitState {
  isLoading: boolean
  isAuthenticated: boolean
  user: IUser | null
}