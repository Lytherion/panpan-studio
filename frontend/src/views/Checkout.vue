<template>
  <div class="checkout-page">
    <el-page-header @back="$router.back()" title="返回">
      <template #content><h2>确认订单</h2></template>
    </el-page-header>

    <div class="checkout-content">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-card header="收货信息" class="form-card">
          <el-form-item label="收件人" prop="recipient_name">
            <el-input v-model="form.recipient_name" placeholder="请输入收件人姓名" />
          </el-form-item>
          <el-form-item label="联系电话" prop="recipient_phone">
            <el-input v-model="form.recipient_phone" placeholder="请输入手机号" />
          </el-form-item>
          <el-form-item label="收货地址" prop="recipient_address">
            <el-input
              v-model="form.recipient_address"
              type="textarea"
              :rows="3"
              placeholder="请输入详细地址"
            />
          </el-form-item>
        </el-card>

        <el-card header="商品清单" class="order-items">
          <el-table :data="cartStore.items" :show-header="false">
            <el-table-column>
              <template #default="{ row }">
                <div class="item-info">
                  <span>{{ row.product_title }} ({{ row.size_name }})</span>
                  <span>x{{ row.quantity }}</span>
                  <span class="price">¥{{ row.subtotal }}</span>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </el-card>

        <el-card class="summary-card">
          <div class="summary-row">
            <span>商品总价:</span>
            <span>¥{{ cartStore.totalAmount }}</span>
          </div>
          <div class="summary-row">
            <span>运费:</span>
            <span>¥10</span>
          </div>
          <el-divider />
          <div class="summary-row total">
            <span>实付金额:</span>
            <span class="amount">¥{{ (cartStore.totalAmount + 10).toFixed(2) }}</span>
          </div>
        </el-card>

        <el-button type="primary" size="large" @click="handleSubmit" :loading="loading" style="width: 100%">
          提交订单
        </el-button>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { createOrder } from '@/api/order'
import { ElMessage } from 'element-plus'

const router = useRouter()
const cartStore = useCartStore()
const formRef = ref()
const loading = ref(false)

const form = reactive({
  recipient_name: '',
  recipient_phone: '',
  recipient_address: ''
})

const rules = {
  recipient_name: [{ required: true, message: '请输入收件人', trigger: 'blur' }],
  recipient_phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
  ],
  recipient_address: [{ required: true, message: '请输入收货地址', trigger: 'blur' }]
}

const handleSubmit = async () => {
  await formRef.value.validate()

  loading.value = true
  try {
    const items = cartStore.items.map(item => ({
      product_id: item.product_id,
      size_id: item.size_id,
      quantity: item.quantity
    }))

    const order = await createOrder({
      ...form,
      items
    })

    ElMessage.success('订单创建成功')
    router.push(`/order/${order.id}`)
  } catch (error) {
    ElMessage.error('订单创建失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  cartStore.fetchCart()
})
</script>

<style scoped>
.checkout-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background: white;
  min-height: 100vh;
}

.checkout-content {
  margin-top: 30px;
}

.form-card, .order-items, .summary-card {
  margin-bottom: 20px;
}

.item-info {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
}

.item-info .price {
  color: #f56c6c;
  font-weight: bold;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin: 15px 0;
  font-size: 16px;
}

.summary-row.total {
  font-size: 20px;
  font-weight: bold;
}

.amount {
  color: #f56c6c;
  font-weight: bold;
}
</style>
