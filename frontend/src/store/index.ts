import { configureStore } from '@reduxjs/toolkit'
import { rootReducer } from '@/store/root-reducer'
import { orderApi } from '@/store/api/order.api'
import { adminUsersApi } from '@/store/api/admin.users.api'
import { adminToolsApi } from '@/store/api/admin.tools.api'


export const store = configureStore({
  reducer: rootReducer,
  devTools: true,
  middleware: getDefaultMiddleware =>
    getDefaultMiddleware()
      .concat(orderApi.middleware)
      .concat(adminUsersApi.middleware)
      .concat(adminToolsApi.middleware)
})


export type RootState = ReturnType<typeof rootReducer>