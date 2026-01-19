<template>
  <div class="admin-products">
    <div class="toolbar">
      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>
        新增商品
      </el-button>
    </div>

    <el-table :data="products" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column label="商品图片" width="100">
        <template #default="{ row }">
          <img :src="getImage(row.images)" class="product-image" />
        </template>
      </el-table-column>
      <el-table-column prop="title" label="商品标题" />
      <el-table-column label="价格区间" width="120">
        <template #default="{ row }">
          ¥{{ getPriceRange(row.sizes) }}
        </template>
      </el-table-column>
      <el-table-column label="总库存" width="100">
        <template #default="{ row }">
          {{ getTotalStock(row.sizes) }}
        </template>
      </el-table-column>
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'">
            {{ row.is_active ? '上架' : '下架' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button text type="primary" @click="handleEdit(row)">编辑</el-button>
          <el-button text type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑商品' : '新增商品'" width="60%">
      <el-form :model="form" label-width="100px">
        <el-form-item label="商品标题">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="商品描述">
          <el-input v-model="form.description" type="textarea" :rows="4" />
        </el-form-item>
        <el-form-item label="商品图片">
          <el-upload
            :file-list="fileList"
            list-type="picture-card"
            :on-success="handleUploadSuccess"
            :on-remove="handleRemove"
            :action="`/api/admin/products/upload`"
            :headers="{ Authorization: `Bearer ${userStore.token}` }"
          >
            <el-icon><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="尺码与价格">
          <el-button @click="addSize" style="margin-bottom: 10px">添加尺码</el-button>
          <div v-for="(size, index) in form.sizes" :key="index" class="size-row">
            <el-input v-model="size.size_name" placeholder="尺码" style="width: 120px" />
            <el-input-number v-model="size.price" :min="0" :precision="2" placeholder="价格" />
            <el-input-number v-model="size.stock" :min="0" placeholder="库存" />
            <el-button text type="danger" @click="removeSize(index)">删除</el-button>
          </div>
        </el-form-item>
        <el-form-item label="是否上架">
          <el-switch v-model="form.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { getProducts, createProduct, updateProduct, deleteProduct } from '@/api/product'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

const userStore = useUserStore()
const products = ref([])
const dialogVisible = ref(false)
const fileList = ref([])
const uploadedImages = ref([])

const form = reactive({
  id: null,
  title: '',
  description: '',
  images: '',
  video_url: '',
  is_active: true,
  sizes: []
})

const fetchProducts = async () => {
  const res = await getProducts()
  products.value = res
}

const getImage = (images) => {
  if (!images) return '/placeholder.jpg'
  const list = JSON.parse(images)
  return list[0] ? `/uploads/${list[0]}` : '/placeholder.jpg'
}

const getPriceRange = (sizes) => {
  if (!sizes || !sizes.length) return '0'
  const prices = sizes.map(s => s.price)
  return `${Math.min(...prices)} - ${Math.max(...prices)}`
}

const getTotalStock = (sizes) => {
  if (!sizes || !sizes.length) return 0
  return sizes.reduce((sum, s) => sum + s.stock, 0)
}

const handleAdd = () => {
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row) => {
  form.id = row.id
  form.title = row.title
  form.description = row.description
  form.images = row.images
  form.video_url = row.video_url
  form.is_active = row.is_active
  form.sizes = row.sizes.map(s => ({ ...s }))

  if (row.images) {
    const images = JSON.parse(row.images)
    fileList.value = images.map((img, index) => ({
      name: `image${index}`,
      url: `/uploads/${img}`
    }))
    uploadedImages.value = [...images]
  }

  dialogVisible.value = true
}

const handleDelete = async (id) => {
  await ElMessageBox.confirm('确定要删除这个商品吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
  await deleteProduct(id)
  ElMessage.success('删除成功')
  fetchProducts()
}

const handleUploadSuccess = (response) => {
  uploadedImages.value.push(response.file_path)
}

const handleRemove = (file) => {
  const url = file.response?.file_path || file.url.replace('/uploads/', '')
  const index = uploadedImages.value.indexOf(url)
  if (index > -1) {
    uploadedImages.value.splice(index, 1)
  }
}

const addSize = () => {
  form.sizes.push({ size_name: '', price: 0, stock: 0 })
}

const removeSize = (index) => {
  form.sizes.splice(index, 1)
}

const handleSave = async () => {
  form.images = JSON.stringify(uploadedImages.value)

  if (form.id) {
    await updateProduct(form.id, form)
    ElMessage.success('更新成功')
  } else {
    await createProduct(form)
    ElMessage.success('创建成功')
  }

  dialogVisible.value = false
  fetchProducts()
}

const resetForm = () => {
  form.id = null
  form.title = ''
  form.description = ''
  form.images = ''
  form.video_url = ''
  form.is_active = true
  form.sizes = []
  fileList.value = []
  uploadedImages.value = []
}

onMounted(fetchProducts)
</script>

<style scoped>
.admin-products {
  padding: 20px;
}

.toolbar {
  margin-bottom: 20px;
}

.product-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}

.size-row {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 10px;
}
</style>
