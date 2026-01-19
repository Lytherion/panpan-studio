<template>
  <div class="order-detail-page" v-if="order">
    <el-page-header @back="$router.back()" title="返回">
      <template #content><h2>订单详情</h2></template>
    </el-page-header>

    <div class="order-content">
      <el-card header="订单信息">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="订单号">{{ order.order_no }}</el-descriptions-item>
          <el-descriptions-item label="订单状态">
            <el-tag :type="getStatusType(order.status)">{{ getStatusText(order.status) }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="下单时间">{{ formatDate(order.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="实付金额">
            <span class="amount">¥{{ order.final_amount }}</span>
          </el-descriptions-item>
        </el-descriptions>
      </el-card>

      <el-card header="收货信息">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="收件人">{{ order.recipient_name }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ order.recipient_phone }}</el-descriptions-item>
          <el-descriptions-item label="收货地址">{{ order.recipient_address }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <el-card header="商品清单">
        <el-table :data="order.items" stripe>
          <el-table-column prop="product_title" label="商品名称" />
          <el-table-column prop="size_name" label="尺码" width="100" />
          <el-table-column prop="price" label="单价" width="120">
            <template #default="{ row }">¥{{ row.price }}</template>
          </el-table-column>
          <el-table-column prop="quantity" label="数量" width="100" />
          <el-table-column prop="subtotal" label="小计" width="120">
            <template #default="{ row }">¥{{ row.subtotal }}</template>
          </el-table-column>
        </el-table>
      </el-card>

      <el-card v-if="order.status === 'pending_payment'" header="付款信息">
        <el-alert title="请通过银行转账完成付款,并上传转账截图" type="info" :closable="false" />
        <div class="payment-info">
          <p><strong>银行名称:</strong> 中国工商银行</p>
          <p><strong>银行卡号:</strong> 6222 0000 0000 0000</p>
          <p><strong>收款人:</strong> 张三</p>
          <p><strong>转账备注:</strong> {{ order.order_no }}</p>
        </div>
        <el-upload
          class="upload-section"
          :action="`/api/orders/${order.id}/payment`"
          :headers="{ 'X-Session-Id': sessionId }"
          :on-success="handleUploadSuccess"
          :show-file-list="false"
          accept="image/*"
        >
          <el-button type="primary">上传付款截图</el-button>
        </el-upload>
      </el-card>

      <el-card v-if="order.payment_image">
        <template #header>付款凭证</template>
        <img :src="`/uploads/${order.payment_image}`" class="payment-image" />
      </el-card>

      <el-card v-if="order.status === 'rejected' && order.reject_reason">
        <template #header>拒绝原因</template>
        <el-alert :title="order.reject_reason" type="error" :closable="false" />
      </el-card>

      <el-card v-if="order.tracking_no">
        <template #header>物流信息</template>
        <p><strong>物流单号:</strong> {{ order.tracking_no }}</p>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getOrder } from '@/api/order'
import { ElMessage } from 'element-plus'

const route = useRoute()
const order = ref(null)
const sessionId = localStorage.getItem('session_id')

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

const fetchOrder = async () => {
  order.value = await getOrder(route.params.id)
}

const handleUploadSuccess = () => {
  ElMessage.success('付款凭证上传成功,请等待审核')
  fetchOrder()
}

onMounted(fetchOrder)
</script>

<style scoped>
.order-detail-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  background: white;
  min-height: 100vh;
}

.order-content {
  margin-top: 30px;
}

.order-content .el-card {
  margin-bottom: 20px;
}

.amount {
  color: #f56c6c;
  font-weight: bold;
  font-size: 18px;
}

.payment-info {
  margin: 20px 0;
  line-height: 2;
}

.upload-section {
  margin-top: 20px;
}

.payment-image {
  max-width: 100%;
  border-radius: 8px;
}
</style>
