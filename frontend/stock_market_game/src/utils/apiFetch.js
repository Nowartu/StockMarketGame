import { authStore } from "@/stores/auth.js";

const API_URL = "http://localhost:8000";

export async function apiFetch(url, options = {}) {
  const store = await authStore()

  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  }

  if (store.access){
    headers.Authorization = `Bearer ${store.access}`
  }

  let response = await fetch(API_URL + url, {
    ...options,
    headers,
  })

  console.log("AA")

  if (response.status === 401 && store.refresh) {
    try {
      await store.refreshToken()
      headers.Authorization = `Bearer ${store.access}`

      response = await fetch(API_URL + url, {
        ...options,
        headers,
      })
    } catch {
      await store.logout()
      throw new Error("Could not retrieve data from the server")
    }
  }

  if(!response.ok){
    const text = await response.text()
    throw new Error(text || response.status)
  }

  return response.json()
}

