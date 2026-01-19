<template>
  <div class="orders-page">
    <el-page-header @back="$router.push('/')" title="返回">
      <template #content><h2>我的订单</h2></template>
    </el-page-header>

    <div class="orders-content">
      <el-empty v-if="!orders.length" description="暂无订单" />

      <el-card v-for="order in orders" :key="order.id" class="order-card" @click="goToDetail(order.id)">
        <template #header>
          <div class="order-header">
            <span>订单号: {{ order.order_no }}</span>
            <el-tag :type="getStatusType(order.status)">{{ getStatusText(order.status) }}</el-tag>
          </div>
        </template>

        <div class="order-info">
          <div class="info-row">
            <span>收件人: {{ order.recipient_name }}</span>
            <span>联系电话: {{ order.recipient_phone }}</span>
          </div>
          <div class="info-row">
            <span>下单时间: {{ formatDate(order.created_at) }}</span>
            <span class="amount">实付金额: ¥{{ order.final_amount }}</span>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getOrders } from '@/api/order'

const router = useRouter()
const orders = ref([])

const statusMap = {
  pending_payment: { text: '待付款', type: 'warning' },
  pending_review: { text: '待审核', type: 'info' },
  confirmed: { text: '已确认', type: 'success' },
  rejected: { text: '已拒绝', type: 'danger' },
  shipped: { text: '已发货', type: 'success' }
}

const getStatusText = (status) => statusMap[status]?.text || status
const getStatusType = (status) => statusMap[status]?.type || 'info'

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

const goToDetail = (id) => {
  router.push(`/order/${id}`)
}

const fetchOrders = async () => {
  orders.value = await getOrders()
}

onMounted(fetchOrders)
</script>

<style scoped>
.orders-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  background: white;
  min-height: 100vh;
}

.orders-content {
  margin-top: 30px;
}

.order-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.order-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-info {
  color: #606266;
}

.info-row {
  display: flex;
  justify-content: space-between;
  margin: 10px 0;
}

.amount {
  color: #f56c6c;
  font-weight: bold;
  font-size: 18px;
}
</style>
