# 穿戴甲电商系统 API 文档

## 项目概述

这是一个基于 FastAPI 的穿戴甲(美甲)电商系统后端,提供完整的商品管理、购物车、订单处理等功能。

## 技术栈

- **框架**: FastAPI 0.115.5
- **数据库**: SQLite (异步)
- **ORM**: SQLAlchemy 2.0
- **认证**: JWT (python-jose)
- **密码加密**: Passlib (bcrypt)
- **图片处理**: Pillow

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 到 `.env` 并修改配置:

```bash
cp .env.example .env
```

### 3. 运行项目

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 访问文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 5. 默认管理员账号

- 用户名: `admin`
- 密码: `admin123`

## API 接口说明

### 前台接口 (Public API)

#### 1. 商品接口

**获取商品列表**
```
GET /api/products?skip=0&limit=50
```

**获取商品详情**
```
GET /api/products/{product_id}
```

#### 2. 购物车接口

所有购物车接口需要在请求头中携带 `X-Session-Id` (可以是任意唯一字符串,用于标识用户)

**获取购物车**
```
GET /api/cart
Headers: X-Session-Id: {session_id}
```

**添加到购物车**
```
POST /api/cart
Headers: X-Session-Id: {session_id}
Body: {
  "product_id": 1,
  "size_id": 1,
  "quantity": 1
}
```

**更新购物车项**
```
PUT /api/cart/{cart_id}
Headers: X-Session-Id: {session_id}
Body: {
  "quantity": 2
}
```

**删除购物车项**
```
DELETE /api/cart/{cart_id}
Headers: X-Session-Id: {session_id}
```

**清空购物车**
```
DELETE /api/cart
Headers: X-Session-Id: {session_id}
```

#### 3. 订单接口

**创建订单**
```
POST /api/orders
Headers: X-Session-Id: {session_id}
Body: {
  "recipient_name": "张三",
  "recipient_phone": "13800138000",
  "recipient_address": "北京市朝阳区xxx",
  "items": [
    {
      "product_id": 1,
      "size_id": 1,
      "quantity": 1
    }
  ]
}
```

**获取订单列表**
```
GET /api/orders
Headers: X-Session-Id: {session_id}
```

**获取订单详情**
```
GET /api/orders/{order_id}
Headers: X-Session-Id: {session_id}
```

**上传付款凭证**
```
POST /api/orders/{order_id}/payment
Headers: X-Session-Id: {session_id}
Body: form-data
  file: (图片文件)
```

### 管理员接口 (Admin API)

所有管理员接口需要在请求头中携带 JWT Token: `Authorization: Bearer {token}`

#### 1. 认证接口

**管理员登录**
```
POST /api/admin/auth/login
Body: {
  "username": "admin",
  "password": "admin123"
}
Response: {
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### 2. 商品管理接口

**创建商品**
```
POST /api/admin/products
Headers: Authorization: Bearer {token}
Body: {
  "title": "美甲产品A",
  "description": "产品描述",
  "images": "[\"products/image1.jpg\", \"products/image2.jpg\"]",
  "video_url": "products/video.mp4",
  "sizes": [
    {
      "size_name": "S",
      "price": 29.9,
      "stock": 100
    },
    {
      "size_name": "M",
      "price": 39.9,
      "stock": 50
    }
  ]
}
```

**更新商品**
```
PUT /api/admin/products/{product_id}
Headers: Authorization: Bearer {token}
Body: (同创建商品)
```

**删除商品**
```
DELETE /api/admin/products/{product_id}
Headers: Authorization: Bearer {token}
```

**上传商品图片/视频**
```
POST /api/admin/products/upload
Headers: Authorization: Bearer {token}
Body: form-data
  file: (图片/视频文件)
Response: {
  "file_path": "products/xxx.jpg"
}
```

#### 3. 订单管理接口

**获取所有订单**
```
GET /api/admin/orders?skip=0&limit=50
Headers: Authorization: Bearer {token}
```

**获取订单详情**
```
GET /api/admin/orders/{order_id}
Headers: Authorization: Bearer {token}
```

**审核订单**
```
POST /api/admin/orders/{order_id}/review?approved=true&reject_reason=原因
Headers: Authorization: Bearer {token}
```

**更新订单状态**
```
PUT /api/admin/orders/{order_id}
Headers: Authorization: Bearer {token}
Body: {
  "status": "shipped",
  "tracking_no": "SF1234567890"
}
```

## 订单状态流转

1. `pending_payment` - 待付款 (订单创建后)
2. `pending_review` - 待审核 (用户上传付款凭证后)
3. `confirmed` - 已确认 (管理员审核通过)
4. `rejected` - 已拒绝 (管理员拒绝)
5. `shipped` - 已发货 (管理员更新物流单号)

## 数据库模型

### User (用户表)
- id: 主键
- username: 用户名
- hashed_password: 加密密码
- is_admin: 是否管理员
- created_at: 创建时间

### Product (商品表)
- id: 主键
- title: 商品标题
- description: 商品描述
- images: 图片列表 (JSON字符串)
- video_url: 视频链接
- is_active: 是否上架
- created_at: 创建时间
- updated_at: 更新时间

### ProductSize (商品尺码表)
- id: 主键
- product_id: 商品ID
- size_name: 尺码名称
- price: 价格
- stock: 库存

### Cart (购物车表)
- id: 主键
- session_id: 会话ID
- product_id: 商品ID
- size_id: 尺码ID
- quantity: 数量
- created_at: 创建时间

### Order (订单表)
- id: 主键
- order_no: 订单号
- session_id: 会话ID
- recipient_name: 收件人姓名
- recipient_phone: 收件人电话
- recipient_address: 收件地址
- total_amount: 商品总价
- shipping_fee: 运费
- final_amount: 实付金额
- status: 订单状态
- payment_image: 付款凭证
- reject_reason: 拒绝原因
- tracking_no: 物流单号
- created_at: 创建时间
- updated_at: 更新时间

### OrderItem (订单项表)
- id: 主键
- order_id: 订单ID
- product_id: 商品ID
- size_id: 尺码ID
- product_title: 商品标题
- size_name: 尺码名称
- price: 单价
- quantity: 数量
- subtotal: 小计

## 安全性说明

1. **管理员认证**: 使用JWT Token进行身份验证
2. **密码加密**: 使用bcrypt算法加密存储
3. **文件上传**: 限制文件大小和类型,防止恶意上传
4. **库存控制**: 下单时锁定库存,防止超卖
5. **权限控制**: 管理员接口需要验证管理员权限

## 部署建议

1. 修改 `.env` 中的 `SECRET_KEY` 为强随机字符串
2. 修改默认管理员密码
3. 配置 HTTPS
4. 使用 PostgreSQL 或 MySQL 替代 SQLite (生产环境)
5. 配置反向代理 (Nginx)
6. 启用日志记录
7. 配置备份策略

## 注意事项

- 商品图片需要以JSON数组字符串格式存储: `["path1.jpg", "path2.jpg"]`
- 购物车使用 `X-Session-Id` 标识用户,前端需要自行生成并保存
- 订单创建后会自动锁定库存,审核拒绝会回滚库存
- 文件上传后返回相对路径,访问时需要加上 `/uploads/` 前缀
