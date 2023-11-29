import { createAsyncThunk } from '@reduxjs/toolkit'
import { ILoginData, ITokens, IUser, IUserAuth, IUserBase, IUserData } from '@/interfaces/user.interface'
import { userService } from '@/services/user.service'

export const register = createAsyncThunk<void, IUserData>(
  'auth/register',
  async (user, thunkApi) => {
    try {
      await userService.register(user)
    } catch (e) {
      console.log(e)
      return thunkApi.rejectWithValue(e)
    }
  }
)

export const login = createAsyncThunk<IUserAuth, ILoginData>(
  'auth/login',
  async (loginData, thunkApi) => {
    try {
      const res = await userService.login(loginData)
      thunkApi.fulfillWithValue(res)
      return res
    } catch (e) {
      console.log(e)
      return thunkApi.rejectWithValue(e)
    }
  }
)

export const verify = createAsyncThunk<IUser, ITokens>(
  'auth/verify',
  async (tokens, thunkApi) => {
    try {
      const res = await userService.verify(tokens)
      thunkApi.fulfillWithValue(res)
      return res
    } catch (e) {
      try {
        refresh(tokens)
      } catch (e) {
        return thunkApi.rejectWithValue(e)
      }
      return thunkApi.rejectWithValue(e)
    }
  }
)

export const refresh = createAsyncThunk<IUserAuth, ITokens>(
  'auth/refresh',
  async (tokens, thunkApi) => {
    try {
      const res = await userService.refresh(tokens)
      thunkApi.fulfillWithValue(res)
      return res
    } catch (e) {
      console.log(e)
      return thunkApi.rejectWithValue(e)
    }
  }
)

export const updateProfile = createAsyncThunk<IUser, IUserBase>(
  'auth/updateProfile',
  async (data, thunkApi) => {
    try {
      const res = await userService.updateProfile(data)
      thunkApi.fulfillWithValue(res)
      return res
    } catch (e) {
      return thunkApi.rejectWithValue(e)
    }
  })