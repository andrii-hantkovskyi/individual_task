import { combineReducers } from '@reduxjs/toolkit'
import { authSlice } from '@/store/auth/auth.slice'
import { orderApi } from '@/store/api/order.api'
import { adminUsersApi } from '@/store/api/admin.users.api'
import { adminToolsApi } from '@/store/api/admin.tools.api'

export const rootReducer = combineReducers({
  auth: authSlice.reducer,
  [orderApi.reducerPath]: orderApi.reducer,
  [adminUsersApi.reducerPath]: adminUsersApi.reducer,
  [adminToolsApi.reducerPath]: adminToolsApi.reducer
})