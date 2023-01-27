import { apiFetch } from "@/globals"
import type { Category } from "@/interfaces/categories"

export const loadCategories = async (token: string): Promise<Category[]> => {
  const response = await apiFetch('/api/categories', {
    headers: { Authorization: `Bearer ${token}` }
  })
  return response as Category[]
}

export const createCategory = async (token: )