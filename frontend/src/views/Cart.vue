<template>
  <div class="cart-page">
    <el-page-header @back="$router.back()" title="返回">
      <template #content>
        <h2>购物车</h2>
      </template>
    </el-page-header>

    <div class="cart-content">
      <el-empty v-if="!cartStore.items.length" description="购物车是空的" />

      <div v-else>
        <el-table :data="cartStore.items" stripe>
          <el-table-column label="商品" width="300">
            <template #default="{ row }">
              <div class="product-info">
                <img :src="`/uploads/${row.image}`" class="product-image" />
                <div>
                  <div>{{ row.product_title }}</div>
                  <el-tag size="small">{{ row.size_name }}</el-tag>
                </div>
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="price" label="单价" width="120">
            <template #default="{ row }">¥{{ row.price }}</template>
          </el-table-column>

          <el-table-column label="数量" width="180">
            <template #default="{ row }">
              <el-input-number
                v-model="row.quantity"
                :min="1"
                size="small"
                @change="handleUpdateQuantity(row)"
              />
            </template>
          </el-table-column>

          <el-table-column prop="subtotal" label="小计" width="120">
            <template #default="{ row }">¥{{ row.subtotal }}</template>
          </el-table-column>

          <el-table-column label="操作" width="100">
            <template #default="{ row }">
              <el-button type="danger" text @click="handleRemove(row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="cart-summary">
          <el-card>
            <div class="summary-item">
              <span>商品总价:</span>
              <span class="amount">¥{{ cartStore.totalAmount }}</span>
            </div>
            <div class="summary-item">
              <span>运费:</span>
              <span class="amount">¥10</span>
            </div>
            <el-divider />
            <div class="summary-item total">
              <span>实付金额:</span>
              <span class="amount">¥{{ (cartStore.totalAmount + 10).toFixed(2) }}</span>
            </div>
            <el-button type="primary" size="large" style="width: 100%; margin-top: 20px" @click="handleCheckout">
              去结算
            </el-button>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { ElMessageBox } from 'element-plus'

const router = useRouter()
const cartStore = useCartStore()

const handleUpdateQuantity = async (item) => {
  await cartStore.updateItem(item.id, item.quantity)
}

const handleRemove = async (id) => {
  await ElMessageBox.confirm('确定要删除这个商品吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
  await cartStore.removeItem(id)
}

const handleCheckout = () => {
  router.push('/checkout')
}

onMounted(() => {
  cartStore.fetchCart()
})
</script>

<style scoped>
.cart-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  background: white;
}

.cart-content {
  margin-top: 30px;
}

.product-info {
  display: flex;
  gap: 15px;
  align-items: center;
}

.product-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}

.cart-summary {
  margin-top: 30px;
  max-width: 400px;
  margin-left: auto;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  margin: 15px 0;
  font-size: 16px;
}

.summary-item.total {
  font-size: 20px;
  font-weight: bold;
}

.amount {
  color: #f56c6c;
  font-weight: bold;
}
</style>
