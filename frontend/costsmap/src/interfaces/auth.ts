export interface User {
  uuid: string
  username: string
  currency: '$' | '₽'
  language: 'russian' | 'english'
}

export interface TokenPair {
  access_token: string
  refresh_token: string
}

export interface LoginData {
  email: string
  password: string
}

export interface RegistrationData {
  email: string
  password1: string
  password2: string
  currency?: string
}