<template>
  <div class="product-detail">
    <el-page-header @back="$router.back()" title="返回" />

    <div class="content" v-if="product">
      <el-row :gutter="40">
        <el-col :md="12">
          <el-carousel height="400px">
            <el-carousel-item v-for="(img, index) in images" :key="index">
              <img :src="`/uploads/${img}`" class="carousel-image" />
            </el-carousel-item>
          </el-carousel>
        </el-col>

        <el-col :md="12">
          <h1>{{ product.title }}</h1>
          <p class="description">{{ product.description }}</p>

          <el-divider />

          <div class="size-select">
            <h3>选择尺码</h3>
            <el-radio-group v-model="selectedSize">
              <el-radio-button
                v-for="size in product.sizes"
                :key="size.id"
                :label="size.id"
                :disabled="size.stock === 0"
              >
                {{ size.size_name }} - ¥{{ size.price }}
                <span v-if="size.stock === 0">(缺货)</span>
                <span v-else>(库存: {{ size.stock }})</span>
              </el-radio-button>
            </el-radio-group>
          </div>

          <div class="quantity-select">
            <h3>数量</h3>
            <el-input-number v-model="quantity" :min="1" :max="maxStock" />
          </div>

          <div class="price-total">
            <span>总价:</span>
            <span class="price">¥{{ totalPrice }}</span>
          </div>

          <div class="actions">
            <el-button type="primary" size="large" @click="handleAddToCart" :disabled="!selectedSize">
              加入购物车
            </el-button>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { getProduct } from '@/api/product'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()

const product = ref(null)
const selectedSize = ref(null)
const quantity = ref(1)

const images = computed(() => {
  if (!product.value?.images) return []
  return JSON.parse(product.value.images)
})

const selectedSizeObj = computed(() => {
  if (!selectedSize.value || !product.value) return null
  return product.value.sizes.find(s => s.id === selectedSize.value)
})

const maxStock = computed(() => {
  return selectedSizeObj.value?.stock || 1
})

const totalPrice = computed(() => {
  if (!selectedSizeObj.value) return 0
  return (selectedSizeObj.value.price * quantity.value).toFixed(2)
})

const fetchProduct = async () => {
  product.value = await getProduct(route.params.id)
  if (product.value.sizes.length > 0 && product.value.sizes[0].stock > 0) {
    selectedSize.value = product.value.sizes[0].id
  }
}

const handleAddToCart = async () => {
  try {
    await cartStore.addItem({
      product_id: product.value.id,
      size_id: selectedSize.value,
      quantity: quantity.value
    })
    ElMessage.success('已添加到购物车')
    router.push('/cart')
  } catch (error) {
    ElMessage.error('添加失败')
  }
}

onMounted(fetchProduct)
</script>

<style scoped>
.product-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: white;
  min-height: 100vh;
}

.content {
  margin-top: 30px;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

h1 {
  font-size: 28px;
  margin-bottom: 15px;
}

.description {
  color: #606266;
  line-height: 1.6;
}

.size-select, .quantity-select {
  margin: 25px 0;
}

.size-select h3, .quantity-select h3 {
  margin-bottom: 15px;
  font-size: 16px;
}

.price-total {
  margin: 30px 0;
  font-size: 24px;
}

.price-total .price {
  color: #f56c6c;
  font-weight: bold;
  margin-left: 10px;
}

.actions {
  display: flex;
  gap: 15px;
}
</style>
