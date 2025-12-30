import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Activity API
export const activityApi = {
  getAll: () => api.get('/activities/'),
  create: (data: { name: string; order: number; is_active: boolean }) => 
    api.post('/activities/', data),
  update: (id: number, data: Partial<{ name: string; order: number; is_active: boolean }>) => 
    api.patch(`/activities/${id}`, data),
  delete: (id: number) => api.delete(`/activities/${id}`),
  reorder: (activity_ids: number[]) => 
    api.post('/activities/reorder', { activity_ids }),
};

// Session API
export const sessionApi = {
  start: (user_id: number) => api.post('/sessions/start', { user_id }),
  stop: (user_id: number) => api.post('/sessions/stop', { user_id }),
  next: (user_id: number) => api.post('/sessions/next', { user_id }),
  getCurrent: (user_id: number) => api.get(`/sessions/current/${user_id}`),
  getHistory: (user_id: number) => api.get(`/sessions/history/${user_id}`),
};

// User API
export const userApi = {
  create: (tg_id: number) => api.post('/users/', { tg_id }),
  getByTgId: (tg_id: number) => api.get(`/users/${tg_id}`),
};

export default api;