import request from '@/utils/request'

export const getProducts = (params) => {
  return request.get('/products', { params })
}

export const getProduct = (id) => {
  return request.get(`/products/${id}`)
}

export const createProduct = (data) => {
  return request.post('/admin/products', data)
}

export const updateProduct = (id, data) => {
  return request.put(`/admin/products/${id}`, data)
}

export const deleteProduct = (id) => {
  return request.delete(`/admin/products/${id}`)
}

export const uploadFile = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return request.post('/admin/products/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}
