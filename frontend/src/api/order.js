import request from '@/utils/request'

export const createOrder = (data) => {
  return request.post('/orders', data)
}

export const getOrders = () => {
  return request.get('/orders')
}

export const getOrder = (id) => {
  return request.get(`/orders/${id}`)
}

export const uploadPayment = (id, file) => {
  const formData = new FormData()
  formData.append('file', file)
  return request.post(`/orders/${id}/payment`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export const getAllOrders = (params) => {
  return request.get('/admin/orders', { params })
}

export const reviewOrder = (id, approved, reject_reason) => {
  return request.post(`/admin/orders/${id}/review`, null, {
    params: { approved, reject_reason }
  })
}

export const updateOrderStatus = (id, data) => {
  return request.put(`/admin/orders/${id}`, data)
}
