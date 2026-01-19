import request from '@/utils/request'

export const getCart = () => {
  return request.get('/cart')
}

export const addToCart = (data) => {
  return request.post('/cart', data)
}

export const updateCart = (id, data) => {
  return request.put(`/cart/${id}`, data)
}

export const deleteCartItem = (id) => {
  return request.delete(`/cart/${id}`)
}

export const clearCart = () => {
  return request.delete('/cart')
}
