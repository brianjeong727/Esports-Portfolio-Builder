import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'

const api = axios.create({
  baseURL: `${API_BASE}/api`,
})

export default api
