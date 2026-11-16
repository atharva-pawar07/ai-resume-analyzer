
import { apiRequest } from './api'

export async function getCurrentUser() {
  return apiRequest('/api/v1/auth/me')
}

export function logout() {
  localStorage.removeItem('access_token')
}
