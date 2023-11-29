export interface IUserBase {
  first_name: string
  middle_name: string
  last_name: string
  delivery_address: string
  date_of_birth: string
  phone_number: number
}

export interface IUserData extends IUserBase {
  email: string
}

export interface ITokens {
  access_token: string
  refresh_token: string
}

export type TRole = 'user' | 'admin' | 'advanced'

export interface IUser extends IUserData {
  role: TRole
}

export interface IUserAuth extends IUser, ITokens {

}

export interface ILoginData {
  email: string
  password: string
}
