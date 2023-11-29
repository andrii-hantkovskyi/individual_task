import { ITokens } from '@/interfaces/user.interface'

export const getAccessToken = () => localStorage.access_token
export const getRefreshToken = () => localStorage.refresh_token

export const getTokens = (): ITokens => ({
  access_token: getAccessToken(),
  refresh_token: getRefreshToken()
})

export const setAccessToken = (value: string) => {
  localStorage.access_token = value
}
export const setRefreshToken = (value: string) => {
  localStorage.refresh_token = value
}

const removeAccessToken = () => {
  localStorage.access_token = ''
}
const removeRefreshToken = () => {
  localStorage.refresh_token = ''
}

export const clearTokens = () => {
  removeAccessToken()
  removeRefreshToken()
}