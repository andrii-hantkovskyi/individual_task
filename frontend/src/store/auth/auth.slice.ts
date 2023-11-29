import { createSlice } from '@reduxjs/toolkit'
import { IAuthInitState } from '@/store/auth/auth.interface'
import { login, refresh, register, updateProfile, verify } from '@/store/auth/auth.actions'
import { clearTokens, setAccessToken, setRefreshToken } from '@/utils/localStorage'

const initialState: IAuthInitState = {
  isLoading: false,
  isAuthenticated: false,
  user: null
}

export const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout: state => {
      state.isAuthenticated = false
      clearTokens()
    }
  },
  extraReducers: builder => {
    builder.addCase(register.pending, state => {
      state.isLoading = true
    }).addCase(register.fulfilled, state => {
      state.isLoading = false
    }).addCase(register.rejected, state => {
      state.isLoading = false
    }).addCase(login.pending, state => {
      state.isLoading = true
    }).addCase(login.fulfilled, (state, { payload }) => {
      state.isLoading = false
      state.isAuthenticated = true
      state.user = payload
      setAccessToken(payload.access_token)
      setRefreshToken(payload.refresh_token)
    }).addCase(login.rejected, state => {
      state.isLoading = false
      state.isAuthenticated = false
      state.user = null
      clearTokens()
    }).addCase(verify.pending, state => {
      state.isLoading = true
    }).addCase(verify.fulfilled, (state, { payload }) => {
      state.isLoading = false
      state.isAuthenticated = true
      state.user = payload
    }).addCase(verify.rejected, state => {
      state.isLoading = false
      state.isAuthenticated = false
      state.user = null
      clearTokens()
    }).addCase(refresh.pending, state => {
      state.isLoading = true
    }).addCase(refresh.fulfilled, (state, { payload }) => {
      state.isLoading = false
      state.isAuthenticated = true
      state.user = payload
      setAccessToken(payload.access_token)
      setRefreshToken(payload.refresh_token)
    }).addCase(refresh.rejected, state => {
      state.isLoading = false
      state.isAuthenticated = false
      state.user = null
      clearTokens()
    }).addCase(updateProfile.pending, state => {
      state.isLoading = true
    }).addCase(updateProfile.fulfilled, (state, { payload }) => {
      state.isLoading = false
      state.user = payload
    }).addCase(updateProfile.rejected, (state, { payload }) => {
      state.isLoading = false
    })
  }
})

export const authActions = authSlice.actions