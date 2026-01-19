<template>
  <div class="admin-orders">
    <el-table :data="orders" stripe>
      <el-table-column prop="order_no" label="订单号" width="200" />
      <el-table-column prop="recipient_name" label="收件人" width="120" />
      <el-table-column prop="recipient_phone" label="联系电话" width="140" />
      <el-table-column prop="final_amount" label="金额" width="100">
        <template #default="{ row }">¥{{ row.final_amount }}</template>
      </el-table-column>
      <el-table-column label="状态" width="120">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="下单时间" width="180">
        <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
      </el-table-column>
      <el-table-column label="操作" fixed="right">
        <template #default="{ row }">
          <el-button text type="primary" @click="handleView(row)">查看</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="订单详情" width="70%">
      <div v-if="currentOrder">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="订单号">{{ currentOrder.order_no }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(currentOrder.status)">
              {{ getStatusText(currentOrder.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="收件人">{{ currentOrder.recipient_name }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ currentOrder.recipient_phone }}</el-descriptions-item>
          <el-descriptions-item label="收货地址" :span="2">
            {{ currentOrder.recipient_address }}
          </el-descriptions-item>
          <el-descriptions-item label="实付金额">¥{{ currentOrder.final_amount }}</el-descriptions-item>
          <el-descriptions-item label="下单时间">{{ formatDate(currentOrder.created_at) }}</el-descriptions-item>
        </el-descriptions>

        <h3 style="margin: 20px 0">商品清单</h3>
        <el-table :data="currentOrder.items" border>
          <el-table-column prop="product_title" label="商品" />
          <el-table-column prop="size_name" label="尺码" width="100" />
          <el-table-column prop="price" label="单价" width="100">
            <template #default="{ row }">¥{{ row.price }}</template>
          </el-table-column>
          <el-table-column prop="quantity" label="数量" width="80" />
          <el-table-column prop="subtotal" label="小计" width="100">
            <template #default="{ row }">¥{{ row.subtotal }}</template>
          </el-table-column>
        </el-table>

        <div v-if="currentOrder.payment_image" style="margin-top: 20px">
          <h3>付款凭证</h3>
          <img :src="`/uploads/${currentOrder.payment_image}`" style="max-width: 400px; margin-top: 10px" />
        </div>

        <div v-if="currentOrder.status === 'pending_review'" class="review-actions">
          <el-button type="success" @click="handleReview(true)">通过审核</el-button>
          <el-button type="danger" @click="handleReview(false)">拒绝订单</el-button>
        </div>

        <div v-if="currentOrder.status === 'confirmed'" class="shipping-actions">
          <el-input v-model="trackingNo" placeholder="输入物流单号" style="width: 300px; margin-right: 10px" />
          <el-button type="primary" @click="handleShip">确认发货</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAllOrders, reviewOrder, updateOrderStatus } from '@/api/order'
import { ElMessage, ElMessageBox } from 'element-plus'

const orders = ref([])
const dialogVisible = ref(false)
const currentOrder = ref(null)
const trackingNo = ref('')

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

const fetchOrders = async () => {
  orders.value = await getAllOrders()
}

const handleView = async (order) => {
  currentOrder.value = order
  dialogVisible.value = true
}

const handleReview = async (approved) => {
  let rejectReason = ''
  if (!approved) {
    const result = await ElMessageBox.prompt('请输入拒绝原因', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消'
    })
    rejectReason = result.value
  }

  await reviewOrder(currentOrder.value.id, approved, rejectReason)
  ElMessage.success(approved ? '审核通过' : '已拒绝订单')
  dialogVisible.value = false
  fetchOrders()
}

const handleShip = async () => {
  if (!trackingNo.value) {
    ElMessage.error('请输入物流单号')
    return
  }

  await updateOrderStatus(currentOrder.value.id, {
    status: 'shipped',
    tracking_no: trackingNo.value
  })
  ElMessage.success('已确认发货')
  dialogVisible.value = false
  fetchOrders()
}

onMounted(fetchOrders)
</script>

<style scoped>
.admin-orders {
  padding: 20px;
}

.review-actions, .shipping-actions {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #dcdfe6;
}
</style>
