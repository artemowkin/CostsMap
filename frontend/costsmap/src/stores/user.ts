import type { Ref } from 'vue'
import type { User, TokenPair } from '@/interfaces/auth'
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import { refreshTokens, loadCurrentUser } from '@/api/auth'

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
      throw err
    }
  }

  return wrapper
}

export const useUserStore = defineStore('user', () => {
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const currentUser = ref<User | null>(null)

  const refresh = _resetStoreOnError(async () => {
    _redirectNotAuthorized(accessToken.value, refreshToken.value)

    const tokenPair = await refreshTokens()

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
  persist: true
})
