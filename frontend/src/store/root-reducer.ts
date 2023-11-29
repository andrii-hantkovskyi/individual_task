import { combineReducers } from '@reduxjs/toolkit'
import { authSlice } from '@/store/auth/auth.slice'
import { orderApi } from '@/store/api/order.api'
import { adminUserApi } from '@/store/api/admin.user.api'

export const rootReducer = combineReducers({
  auth: authSlice.reducer,
  [orderApi.reducerPath]: orderApi.reducer,
  [adminUserApi.reducerPath]: adminUserApi.reducer
})