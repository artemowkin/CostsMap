import type { User, LoginData, RegistrationData, TokenPair } from "@/interfaces/auth"
import { apiFetch } from "@/globals"
import cookieStorage from "@/stores/cookieStorage"

type ErrorEvent = (msg: string, code?: number) => void

function handleAuthErrors<T, R>(
  func: (data: T) => Promise<R>
): (data: T, onError?: ErrorEvent) => Promise<R> {
  const wrapper = async (data: T, onError?: ErrorEvent): Promise<R> => {
    try {
      return await func(data)
    } catch (err: any) {
      if (!err?.response) throw err

      switch (err?.response?.status) {
        case 422:
          if (onError) onError("Incorrect input", 422)
          throw err
        case 401:
          if (onError) onError("Incorrect username or password", 401)
          throw err
        case 409:
          if (onError) onError("User with this email already exists", 409)
        default:
          if (onError) onError("Server error", err.repsonse.status)
          throw err
      }
    }
  }

  return wrapper
}

export const login = handleAuthErrors<LoginData, TokenPair>(async (
    data: LoginData): Promise<TokenPair> => {
  const response: TokenPair = await apiFetch('/api/auth/login', {
    body: data,
    method: 'POST'
  })
  cookieStorage.setItem('refresh_token', response.refresh_token)
  return response
})

export const registrate = handleAuthErrors<RegistrationData, TokenPair>(async (
    data: RegistrationData): Promise<TokenPair> => {
  const response: TokenPair = await apiFetch('/api/auth/registration', {
    body: data,
    method: 'POST'
  })
  cookieStorage.setItem('refresh_token', response.refresh_token)
  return response
})

export const refreshTokens = handleAuthErrors<void, TokenPair | void>(async (): Promise<TokenPair | void> => {
  const tokenPair = await apiFetch('/api/auth/refresh', {
    credentials: 'include',
    method: 'POST'
  })

  return tokenPair
})

export const loadCurrentUser = handleAuthErrors<string, User | void>(async (accessToken: string): Promise<User | void> => {
  const response = await apiFetch('/api/auth/me', {
    headers: { Authorization: `Bearer ${accessToken}` }
  })

  return response
})