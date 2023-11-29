import * as AuthThunkActions from './auth/auth.actions'
import { authActions } from './auth/auth.slice'


export const RootAction = {
  ...AuthThunkActions,
  ...authActions
}