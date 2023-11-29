import { configureStore } from '@reduxjs/toolkit'
import { rootReducer } from '@/store/root-reducer'
import { orderApi } from '@/store/api/order.api'


export const store = configureStore({
  reducer: rootReducer,
  devTools: true,
  middleware: getDefaultMiddleware => getDefaultMiddleware().concat(orderApi.middleware)
})


export type RootState = ReturnType<typeof rootReducer>