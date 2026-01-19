<template>
  <div class="home">
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <h1>穿戴甲商城</h1>
          <div class="header-right">
            <el-button text @click="$router.push('/orders')">我的订单</el-button>
            <el-badge :value="cartStore.totalItems" :hidden="!cartStore.totalItems">
              <el-button type="primary" @click="$router.push('/cart')">
                <el-icon><ShoppingCart /></el-icon>
                购物车
              </el-button>
            </el-badge>
          </div>
        </div>
      </el-header>

      <el-main>
        <div class="banner">
          <h2>精美穿戴甲 轻松变美</h2>
          <p>质量保证 · 快速发货 · 贴心服务</p>
        </div>

        <div class="products">
          <el-row :gutter="20">
            <el-col :xs="12" :sm="8" :md="6" v-for="product in products" :key="product.id">
              <el-card class="product-card" @click="goToDetail(product.id)" shadow="hover">
                <img :src="getProductImage(product.images)" class="product-image" />
                <div class="product-info">
                  <h3>{{ product.title }}</h3>
                  <div class="product-price">¥{{ product.min_price }}</div>
                  <el-tag v-if="!product.in_stock" type="info" size="small">已售罄</el-tag>
                  <el-tag v-else type="success" size="small">有货</el-tag>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </el-main>

      <el-footer class="footer">
        <p>© 2024 穿戴甲商城 · 联系客服微信: xxxxx</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { getProducts } from '@/api/product'
import { ShoppingCart } from '@element-plus/icons-vue'

const router = useRouter()
const cartStore = useCartStore()
const products = ref([])

const fetchProducts = async () => {
  products.value = await getProducts()
}

const getProductImage = (images) => {
  if (!images) return '/placeholder.jpg'
  const imageList = JSON.parse(images)
  return imageList[0] ? `/uploads/${imageList[0]}` : '/placeholder.jpg'
}

const goToDetail = (id) => {
  router.push(`/product/${id}`)
}

onMounted(() => {
  fetchProducts()
  cartStore.fetchCart()
})
</script>

<style scoped>
.home {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.header {
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.header-right {
  display: flex;
  gap: 15px;
  align-items: center;
}

.banner {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
  padding: 60px 20px;
  border-radius: 10px;
  margin-bottom: 40px;
}

.banner h2 {
  font-size: 32px;
  margin-bottom: 10px;
}

.products {
  max-width: 1200px;
  margin: 0 auto;
}

.product-card {
  cursor: pointer;
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.product-card:hover {
  transform: translateY(-5px);
}

.product-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
}

.product-info {
  margin-top: 15px;
}

.product-info h3 {
  font-size: 16px;
  margin-bottom: 10px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-price {
  color: #f56c6c;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 8px;
}

.footer {
  background: white;
  text-align: center;
  color: #909399;
  margin-top: 40px;
}
</style>
