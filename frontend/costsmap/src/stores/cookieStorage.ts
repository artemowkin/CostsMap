import type { StorageLike } from "pinia-plugin-persistedstate"

class CookieStorage implements StorageLike {
  getItem(key: string): string | null {
    const matches = document.cookie.match(new RegExp(
      "(?:^|; )" + key.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ))
    return matches ? decodeURIComponent(matches[1]) : null
  }

  setItem(key: string, value: string): void {
    const tomorrow = new Date(+new Date() + 24*60*60*1000)
    const nextMonth = new Date(+new Date() + 30*24*60*60*1000)
    const expires = key === 'refreshToken' ? nextMonth : tomorrow
    const path = '/'
    let newCookie = encodeURIComponent(key) + '=' + encodeURIComponent(value)
    newCookie += `; expires=${expires}; path=${path}`
    document.cookie = newCookie
  }
}

export default new CookieStorage()