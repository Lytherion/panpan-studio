import request from '@/utils/request'

export const login = (data) => {
  return request.post('/admin/auth/login', data)
}
