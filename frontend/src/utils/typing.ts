import { IUserInfoAdmin } from '@/interfaces/user.interface'

export const isIUserInfoAdmin = (object: any): object is IUserInfoAdmin => {
  return '_id' in object
}