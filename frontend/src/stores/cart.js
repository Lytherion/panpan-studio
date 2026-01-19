import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getCart, addToCart, updateCart, deleteCartItem } from '@/api/cart'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])
  const loading = ref(false)

  const totalItems = computed(() => {
    return items.value.reduce((sum, item) => sum + item.quantity, 0)
  })

  const totalAmount = computed(() => {
    return items.value.reduce((sum, item) => sum + item.subtotal, 0)
  })

  const fetchCart = async () => {
    loading.value = true
    try {
      items.value = await getCart()
    } finally {
      loading.value = false
    }
  }

  const addItem = async (data) => {
    await addToCart(data)
    await fetchCart()
  }

  const updateItem = async (id, quantity) => {
    await updateCart(id, { quantity })
    await fetchCart()
  }

  const removeItem = async (id) => {
    await deleteCartItem(id)
    await fetchCart()
  }

  return {
    items,
    loading,
    totalItems,
    totalAmount,
    fetchCart,
    addItem,
    updateItem,
    removeItem
  }
})
