# 穿戴甲电商系统 - 前端

## 技术栈

- **Vue 3** - 渐进式JavaScript框架
- **Vite** - 下一代前端构建工具
- **Vue Router** - 官方路由管理器
- **Pinia** - 新一代状态管理
- **Element Plus** - Vue 3组件库
- **Axios** - HTTP客户端

## 项目结构

```
frontend/
├── src/
│   ├── api/              # API接口
│   │   ├── auth.js       # 认证接口
│   │   ├── cart.js       # 购物车接口
│   │   ├── order.js      # 订单接口
│   │   └── product.js    # 商品接口
│   ├── stores/           # Pinia状态管理
│   │   ├── cart.js       # 购物车状态
│   │   └── user.js       # 用户状态
│   ├── views/            # 页面组件
│   │   ├── admin/        # 管理员页面
│   │   │   ├── Layout.vue
│   │   │   ├── Login.vue
│   │   │   ├── Orders.vue
│   │   │   └── Products.vue
│   │   ├── Cart.vue
│   │   ├── Checkout.vue
│   │   ├── Home.vue
│   │   ├── OrderDetail.vue
│   │   ├── Orders.vue
│   │   └── ProductDetail.vue
│   ├── router/           # 路由配置
│   │   └── index.js
│   ├── utils/            # 工具函数
│   │   └── request.js    # Axios封装
│   ├── App.vue           # 根组件
│   └── main.js           # 入口文件
├── index.html            # HTML模板
├── package.json          # 依赖配置
└── vite.config.js        # Vite配置
```

## 开发指南

### 安装依赖
```bash
npm install
```

### 开发模式
```bash
npm run dev
```
访问: http://localhost:3000

### 生产构建
```bash
npm run build
```

### 预览构建
```bash
npm run preview
```

## 页面说明

### 前台页面

#### 1. 首页 (`/`)
- 展示商品列表
- 显示购物车数量
- 商品卡片点击进入详情

#### 2. 商品详情 (`/product/:id`)
- 商品图片轮播
- 尺码选择
- 数量选择
- 加入购物车

#### 3. 购物车 (`/cart`)
- 商品列表展示
- 数量修改
- 删除商品
- 金额汇总
- 去结算

#### 4. 结算页 (`/checkout`)
- 填写收货信息
- 商品清单确认
- 提交订单

#### 5. 我的订单 (`/orders`)
- 订单列表
- 订单状态显示
- 点击查看详情

#### 6. 订单详情 (`/order/:id`)
- 订单信息展示
- 上传付款凭证
- 查看物流信息

### 管理员页面

#### 1. 登录 (`/admin/login`)
- 管理员登录
- JWT认证

#### 2. 商品管理 (`/admin/products`)
- 商品列表
- 新增/编辑商品
- 上传图片
- 管理尺码和库存
- 上下架控制

#### 3. 订单管理 (`/admin/orders`)
- 订单列表
- 查看订单详情
- 审核付款凭证
- 更新订单状态
- 填写物流单号

## 状态管理

### Cart Store
```javascript
import { useCartStore } from '@/stores/cart'

const cartStore = useCartStore()

// 获取购物车
await cartStore.fetchCart()

// 添加商品
await cartStore.addItem({ product_id, size_id, quantity })

// 更新数量
await cartStore.updateItem(cart_id, quantity)

// 删除商品
await cartStore.removeItem(cart_id)

// 访问状态
cartStore.items        // 购物车商品
cartStore.totalItems   // 总数量
cartStore.totalAmount  // 总金额
```

### User Store
```javascript
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// 登录
await userStore.login(username, password)

// 登出
userStore.logout()

// 访问状态
userStore.isAdmin  // 是否管理员
userStore.token    // JWT Token
```

## API调用

### 使用封装的request
```javascript
import request from '@/utils/request'

// GET请求
const products = await request.get('/products', { params: { limit: 10 } })

// POST请求
const order = await request.post('/orders', orderData)

// 文件上传
const formData = new FormData()
formData.append('file', file)
const res = await request.post('/admin/products/upload', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
})
```

### 请求拦截器
自动添加:
- Authorization: Bearer Token (管理员接口)
- X-Session-Id: Session ID (用户接口)

### 响应拦截器
自动处理:
- 错误提示
- 数据解包

## 路由守卫

管理员页面自动验证Token:
```javascript
// 访问/admin路径时自动检查登录状态
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('admin_token')

  if (to.path.startsWith('/admin') && to.name !== 'AdminLogin' && !token) {
    next('/admin/login')  // 未登录跳转到登录页
  } else {
    next()
  }
})
```

## 样式规范

### Element Plus主题
使用Element Plus默认主题,可在`main.js`中自定义:

```javascript
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

app.use(ElementPlus, {
  // 自定义配置
})
```

### 组件样式
- 使用scoped样式隔离
- 遵循BEM命名规范
- 响应式设计

## 环境变量

开发环境自动代理到后端API:
```javascript
// vite.config.js
server: {
  proxy: {
    '/api': 'http://localhost:8000',
    '/uploads': 'http://localhost:8000'
  }
}
```

生产环境直接访问同源API。

## 最佳实践

1. **组件化**: 将重复代码提取为组件
2. **状态管理**: 全局状态使用Pinia
3. **错误处理**: 统一在拦截器中处理
4. **加载状态**: 使用loading提示
5. **表单验证**: 使用Element Plus表单验证
6. **图片懒加载**: 大量图片时使用懒加载
7. **路由懒加载**: 使用动态import

## 性能优化

1. **路由懒加载**
```javascript
component: () => import('@/views/Home.vue')
```

2. **图片优化**
- 压缩图片
- 使用WebP格式
- 懒加载

3. **打包优化**
- Tree Shaking
- Code Splitting
- Gzip压缩

## 常见问题

### 1. API请求失败
检查后端是否启动,端口是否正确 (8000)

### 2. 图片不显示
检查图片路径是否正确,后端uploads目录是否存在

### 3. 管理员登录失败
检查用户名密码,默认:
- 用户名: admin
- 密码: admin123

### 4. Session ID错误
清除localStorage并刷新页面

## 扩展开发

### 添加新页面
1. 在`src/views/`创建Vue文件
2. 在`router/index.js`添加路由
3. 在导航菜单中添加链接

### 添加新API
1. 在`src/api/`创建API文件
2. 导出API函数
3. 在组件中调用

### 添加新Store
1. 在`src/stores/`创建Store文件
2. 使用`defineStore`定义
3. 在组件中使用`useXxxStore()`

## 浏览器支持

- Chrome >= 87
- Firefox >= 78
- Safari >= 14
- Edge >= 88

不支持IE浏览器。
