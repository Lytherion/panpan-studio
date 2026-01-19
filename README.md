# 穿戴甲电商系统

一个基于 FastAPI 的穿戴甲(美甲)销售的轻量级电商平台后端系统。

## 功能特性

### 前台功能
- 商品展示与详情查看
- 购物车管理
- 订单创建与管理
- 付款凭证上传
- 订单状态跟踪

### 后台功能
- 管理员认证(JWT)
- 商品管理(CRUD)
- 商品图片/视频上传
- 尺码与库存管理
- 订单管理
- 付款凭证审核
- 订单状态流转

## 技术栈

- **FastAPI** - 现代、高性能的Web框架
- **SQLAlchemy 2.0** - 异步ORM
- **SQLite** - 轻量级数据库
- **JWT** - 用户认证
- **Pillow** - 图片处理

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境

复制 `.env.example` 到 `.env`:

```bash
cp .env.example .env
```

根据需要修改配置项。

### 3. 运行项目

```bash
uvicorn app.main:app --reload
```

服务将在 http://localhost:8000 启动

### 4. 访问文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 5. 默认管理员

- 用户名: `admin`
- 密码: `admin123`

⚠️ **生产环境请务必修改默认密码!**

## 项目结构

```
panpan-studio/
├── app/
│   ├── api/              # API路由
│   │   ├── admin/        # 管理员接口
│   │   ├── products.py   # 商品接口
│   │   ├── cart.py       # 购物车接口
│   │   └── orders.py     # 订单接口
│   ├── models/           # 数据库模型
│   ├── schemas/          # Pydantic模式
│   ├── services/         # 业务逻辑层
│   ├── utils/            # 工具函数
│   ├── config.py         # 配置文件
│   ├── database.py       # 数据库连接
│   └── main.py           # 主应用
├── uploads/              # 上传文件目录
├── requirements.txt      # 依赖包
├── .env                  # 环境变量
└── README.md             # 项目说明
```

## API 文档

详细的API接口文档请查看 [README_API.md](README_API.md)

## 主要接口

### 前台接口
- `GET /api/products` - 获取商品列表
- `GET /api/products/{id}` - 获取商品详情
- `POST /api/cart` - 添加到购物车
- `POST /api/orders` - 创建订单
- `POST /api/orders/{id}/payment` - 上传付款凭证

### 管理员接口
- `POST /api/admin/auth/login` - 管理员登录
- `POST /api/admin/products` - 创建商品
- `PUT /api/admin/products/{id}` - 更新商品
- `POST /api/admin/orders/{id}/review` - 审核订单
- `PUT /api/admin/orders/{id}` - 更新订单状态

## 业务流程

### 用户下单流程
1. 浏览商品列表
2. 查看商品详情,选择尺码
3. 添加到购物车
4. 填写收货信息创建订单
5. 上传付款凭证
6. 等待管理员审核
7. 查看订单状态

### 管理员处理订单流程
1. 登录管理后台
2. 查看待审核订单
3. 查看付款凭证
4. 审核通过/拒绝订单
5. 发货并更新物流单号

## 安全性

- JWT Token认证
- 密码bcrypt加密
- 文件上传大小和类型限制
- 管理员权限验证
- 库存锁定防止超卖

## 部署建议

### 生产环境配置

1. 修改 `SECRET_KEY` 为强随机字符串
2. 修改默认管理员密码
3. 使用 PostgreSQL/MySQL 替代 SQLite
4. 配置 HTTPS
5. 使用 Gunicorn + Uvicorn Workers

### 运行命令

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 开发计划

- [ ] 用户注册登录
- [ ] 微信/支付宝支付
- [ ] 优惠券系统
- [ ] 商品分类与搜索
- [ ] 物流追踪
- [ ] 销量统计

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request!
