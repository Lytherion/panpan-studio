# 快速启动指南

## 📦 一键启动 (推荐)

### Windows
双击运行 `start.bat`

### Linux/Mac
```bash
chmod +x start.sh
./start.sh
```

脚本会自动:
1. 检查Python和Node.js环境
2. 安装后端依赖
3. 安装前端依赖
4. 构建前端
5. 启动服务

## 🌐 访问地址

启动成功后访问:

- **前台商城**: http://localhost:8000
- **管理后台**: http://localhost:8000/admin/login
- **API文档**: http://localhost:8000/docs

## 🔑 默认账号

管理员登录:
- 用户名: `admin`
- 密码: `admin123`

## 🚀 手动启动 (开发调试)

### 1. 启动后端

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动后端
python run.py
```

后端将运行在 http://localhost:8000

### 2. 启动前端 (开发模式)

打开新的终端:

```bash
cd frontend
npm install
npm run dev
```

前端将运行在 http://localhost:3000

开发模式下前端和后端分离,前端会自动代理API请求到后端。

## 📝 测试流程

### 前台测试

1. **浏览商品**
   - 访问首页查看商品列表
   - 点击商品卡片进入详情页

2. **添加购物车**
   - 选择尺码和数量
   - 点击"加入购物车"
   - 查看购物车图标数量变化

3. **查看购物车**
   - 点击顶部购物车按钮
   - 可以修改商品数量或删除商品

4. **创建订单**
   - 点击"去结算"
   - 填写收货信息
   - 提交订单

5. **上传付款凭证**
   - 在订单详情页
   - 点击"上传付款截图"
   - 选择图片上传

6. **查看订单状态**
   - 点击"我的订单"
   - 查看订单列表和详情

### 后台测试

1. **管理员登录**
   - 访问 http://localhost:8000/admin/login
   - 使用admin/admin123登录

2. **商品管理**
   - 点击"商品管理"菜单
   - 新增商品:
     - 填写商品标题和描述
     - 上传商品图片
     - 添加多个尺码和价格
     - 设置库存
     - 保存
   - 编辑/删除商品

3. **订单管理**
   - 点击"订单管理"菜单
   - 查看所有订单列表
   - 点击"查看"查看订单详情
   - 对于"待审核"的订单:
     - 查看付款凭证
     - 点击"通过审核"或"拒绝订单"
   - 对于"已确认"的订单:
     - 填写物流单号
     - 点击"确认发货"

## 🐛 常见问题

### 1. 端口被占用

**问题**: 提示8000端口被占用

**解决**:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <进程ID> /F

# Linux/Mac
lsof -i :8000
kill -9 <进程ID>
```

### 2. 模块未找到

**问题**: ModuleNotFoundError

**解决**: 确保已激活虚拟环境并安装依赖
```bash
pip install -r requirements.txt
```

### 3. 前端无法连接后端

**问题**: API请求失败

**解决**:
- 确保后端已启动 (http://localhost:8000)
- 检查vite.config.js中的proxy配置
- 清除浏览器缓存

### 4. 图片上传失败

**问题**: 上传后图片不显示

**解决**:
- 检查uploads目录是否存在
- 检查文件权限
- 查看浏览器控制台错误信息

### 5. SQLite数据库锁定

**问题**: database is locked

**解决**:
- 关闭所有正在访问数据库的进程
- 删除panpan.db文件重新启动(会丢失数据)

## 🔧 开发建议

### 修改后端代码
- 修改Python代码后,使用Ctrl+C停止服务,重新运行`python run.py`
- 或使用`uvicorn app.main:app --reload`启用热重载

### 修改前端代码
- 开发模式下(`npm run dev`)代码会自动热更新
- 修改后浏览器自动刷新

### 查看日志
- 后端日志: 直接在启动终端查看
- 前端日志: 浏览器F12开发者工具Console

## 📚 下一步

- 阅读 [README.md](README.md) 了解项目详情
- 阅读 [README_API.md](README_API.md) 了解API接口
- 阅读 [DEPLOY.md](DEPLOY.md) 了解生产部署
- 阅读 [frontend/README.md](frontend/README.md) 了解前端开发

## 💡 开发技巧

### 快速测试完整流程

1. 启动项目
2. 后台添加测试商品 (附带图片和多个尺码)
3. 前台浏览商品
4. 加入购物车并下单
5. 上传付款截图
6. 后台审核通过
7. 后台填写物流单号发货
8. 前台查看物流信息

### 数据重置

如需清空所有数据重新测试:
```bash
# 删除数据库文件
rm panpan.db  # Linux/Mac
del panpan.db # Windows

# 清空上传文件
rm -rf uploads/*  # Linux/Mac
rmdir /s uploads  # Windows

# 重新启动,会自动创建数据库和管理员账号
python run.py
```

## 🎉 祝您使用愉快!

如有问题,请查看完整文档或提交Issue。
