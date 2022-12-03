import type { Ref } from 'vue'
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import { apiFetch } from '@/globals'
import cookieStorage from '@/stores/cookieStorage'

interface User {
  uuid: string
  username: string
  currency: '$' | '₽'
  language: 'russian' | 'english'
}

interface TokenPair {
  access_token: string
  refresh_token: string
}

const refreshTokens = async (refreshToken: string): Promise<TokenPair | void> => {
  const { data } = await apiFetch('/api/auth/refresh', {
    headers: { Authorization: `Bearer ${refreshToken}` },
    method: 'POST'
  })

  return data
}

const loadCurrentUser = async (accessToken: string): Promise<User | void> => {
  const response = await apiFetch('/api/auth/me', {
    headers: { Authorization: `Bearer ${accessToken}` }
  })

  return response
}

const _redirectNotAuthorized = (accessToken: string | null, refreshToken: string | null) => {
  const router = useRouter()

  if (!accessToken || !refreshToken) router.push({ name: 'login' })
}

type StoreRefs = {
  accessToken: Ref<string | null>,
  refreshToken: Ref<string | null>,
  currentUser: Ref<User | null>,
}

const _resetStoreOnError = (
  func: () => Promise<void>,
  { accessToken, refreshToken, currentUser }: StoreRefs
) => {
  
  const wrapper = async () => {
    try {
      await func()
    } catch (err) {
      accessToken.value = null
      refreshToken.value = null
      currentUser.value = null
    }
  }

  return wrapper
}

export const useUserStore = defineStore('user', () => {
  const accessToken = ref<string | null>(localStorage.getItem('accessToken'))
  const refreshToken = ref<string | null>(localStorage.getItem('refreshToken'))
  const currentUser = ref<User | null>(null)

  const refresh = _resetStoreOnError(async () => {
    _redirectNotAuthorized(accessToken.value, refreshToken.value)

    const tokenPair = await refreshTokens(refreshToken.value as string)

    if (tokenPair) {
      accessToken.value = tokenPair.access_token
      refreshToken.value = tokenPair.refresh_token
    }
  }, { accessToken, refreshToken, currentUser })

  const load = _resetStoreOnError(async (): Promise<void> => {
    if (!accessToken.value || !refreshToken.value) return

    const user = await loadCurrentUser(accessToken.value as string)

    if (user) currentUser.value = user
  }, { accessToken, refreshToken, currentUser })

  const setTokens = async (tokenPair: TokenPair): Promise<void> => {
    accessToken.value = tokenPair.access_token
    refreshToken.value = tokenPair.refresh_token
    await load()
  }

  return { accessToken, refreshToken, currentUser, refresh, load, setTokens }
}, {
  persist: {
    storage: cookieStorage
  }
})
