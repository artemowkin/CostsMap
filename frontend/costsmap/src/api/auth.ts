import type { LoginData, RegistrationData, TokenPair } from "@/interfaces/auth"
import { apiFetch } from "@/globals"

type ErrorEvent = (msg: string, code?: number) => void

function handleAuthErrors<T>(
  login: (data: T) => Promise<TokenPair>
): (data: T, onError?: ErrorEvent) => Promise<TokenPair> {
  const wrapper = async (data: T, onError?: ErrorEvent): Promise<TokenPair> => {
    try {
      return await login(data)
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

export const login = handleAuthErrors<LoginData>(async (
    data: LoginData): Promise<TokenPair> => {
  const response: TokenPair = await apiFetch('/api/auth/login', {
    body: data,
    method: 'POST'
  })
  return response
})

export const registrate = handleAuthErrors<RegistrationData>(async (
    data: RegistrationData): Promise<TokenPair> => {
  const response: TokenPair = await apiFetch('/api/auth/registration', {
    body: data,
    method: 'POST'
  })
  return response
})