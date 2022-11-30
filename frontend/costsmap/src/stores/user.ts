import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import { apiFetch } from '@/globals'

interface User {
  uuid: string
  username: string
}

interface TokenPair {
  access_token: string
  refresh_token: string
}

const refreshTokens = async (refreshToken: string): Promise<TokenPair | void> => {
  const router = useRouter()

  try {
    const { data } = await apiFetch('/api/auth/refresh', {
      headers: { Authorization: `Bearer ${refreshToken}` },
      method: 'POST'
    })
    return data
  } catch (err) {
    switch (err?.response?.status) {
      case 401:
      case 403:
        router.push({ name: 'login' })
        break
      default:
        throw err
    }
  }
}

const loadCurrentUser = async (accessToken: string, onRefresh: () => void): Promise<User | void> => {
  try {
    const { data } = await apiFetch('/api/auth/me', {
      headers: { Authorization: `Bearer ${accessToken}` }
    })
    return data
  } catch (err) {
    switch (err?.repsonse?.status) {
      case 401:
      case 403:
        onRefresh()
        break
      default:
        throw err
    }
  }
}

const _redirectNotAuthorized = (accessToken: string | null, refreshToken: string | null) => {
  const router = useRouter()

  if (!accessToken || !refreshToken) router.push({ name: 'login' })
}

export const useUserStore = defineStore('user', () => {
  const accessToken = ref<string | null>(localStorage.getItem('accessToken'))
  const refreshToken = ref<string | null>(localStorage.getItem('refreshToken'))
  const currentUser = ref<User | null>(null)

  const refresh = async () => {
    _redirectNotAuthorized(accessToken.value, refreshToken.value)

    const tokenPair = await refreshTokens(refreshToken.value as string)

    if (tokenPair) {
      accessToken.value = tokenPair.access_token
      refreshToken.value = tokenPair.refresh_token
    }
  }

  const load = async (): Promise<boolean | void> => {
    if (!accessToken.value || !refreshToken.value) return false

    const user = await loadCurrentUser(accessToken.value as string, refresh)

    if (user) currentUser.value = user
  }

  return { accessToken, refreshToken, currentUser, refresh, load }
})
