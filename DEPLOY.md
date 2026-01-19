# 穿戴甲电商系统 - 部署指南

## 环境要求

### 必需软件
- Python 3.11+
- Node.js 18+
- npm 或 yarn

### 可选软件
- Git (用于克隆代码)
- PostgreSQL (生产环境推荐)

## 快速开始 (本地测试)

### Windows系统

1. **双击运行启动脚本**
```bash
start.bat
```

2. **访问系统**
- 前台: http://localhost:8000
- 后台: http://localhost:8000/admin/login
- API文档: http://localhost:8000/docs

### Linux/Mac系统

1. **赋予执行权限并运行**
```bash
chmod +x start.sh
./start.sh
```

2. **访问系统**
- 前台: http://localhost:8000
- 后台: http://localhost:8000/admin/login
- API文档: http://localhost:8000/docs

## 手动部署步骤

### 1. 后端部署

#### 创建虚拟环境
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 安装依赖
```bash
pip install -r requirements.txt
```

#### 配置环境变量
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件,修改以下配置:
# - SECRET_KEY: 改为强随机字符串
# - ADMIN_PASSWORD: 修改默认管理员密码
# - DATABASE_URL: 生产环境建议使用PostgreSQL
```

#### 启动后端
```bash
# 开发环境
python run.py

# 生产环境
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### 2. 前端部署

#### 安装依赖
```bash
cd frontend
npm install
```

#### 开发模式 (带热更新)
```bash
npm run dev
```
前端将运行在 http://localhost:3000

#### 生产构建
```bash
npm run build
```

构建完成后,将 `dist` 目录下的文件复制到后端 `app/static` 目录:

```bash
# Windows
xcopy /s /e /y dist\* ..\app\static\

# Linux/Mac
cp -r dist/* ../app/static/
```

## 生产环境部署

### 使用Nginx反向代理

1. **安装Nginx**

2. **配置Nginx**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 上传文件
    location /uploads/ {
        alias /path/to/panpan-studio/uploads/;
    }

    # API接口
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. **配置SSL (可选但推荐)**
```bash
# 使用Let's Encrypt
certbot --nginx -d your-domain.com
```

### 使用Supervisor管理进程

1. **安装Supervisor**
```bash
pip install supervisor
```

2. **创建配置文件** `/etc/supervisor/conf.d/panpan-studio.conf`
```ini
[program:panpan-studio]
command=/path/to/venv/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000
directory=/path/to/panpan-studio
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/panpan-studio.err.log
stdout_logfile=/var/log/panpan-studio.out.log
```

3. **启动服务**
```bash
supervisorctl reread
supervisorctl update
supervisorctl start panpan-studio
```

### 使用Docker部署

1. **创建Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装Node.js
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# 复制项目文件
COPY . .

# 安装Python依赖
RUN pip install -r requirements.txt

# 构建前端
RUN cd frontend && npm install && npm run build && \
    mkdir -p /app/app/static && \
    cp -r dist/* /app/app/static/

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **构建并运行**
```bash
docker build -t panpan-studio .
docker run -d -p 8000:8000 --name panpan-studio panpan-studio
```

## 数据库迁移

### 从SQLite迁移到PostgreSQL

1. **安装PostgreSQL驱动**
```bash
pip install psycopg2-binary asyncpg
```

2. **修改.env配置**
```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost/panpan_db
```

3. **导出SQLite数据** (可选)
```bash
sqlite3 panpan.db .dump > backup.sql
```

## 备份策略

### 数据库备份
```bash
# SQLite
cp panpan.db panpan_backup_$(date +%Y%m%d).db

# PostgreSQL
pg_dump panpan_db > backup_$(date +%Y%m%d).sql
```

### 上传文件备份
```bash
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz uploads/
```

## 性能优化

### 1. 数据库优化
- 使用PostgreSQL替代SQLite
- 配置数据库连接池
- 添加适当的索引

### 2. 静态资源优化
- 使用CDN托管静态资源
- 启用Gzip压缩
- 配置浏览器缓存

### 3. 服务器优化
- 使用多进程Gunicorn
- 配置合适的Worker数量 (CPU核心数 * 2 + 1)
- 启用缓存 (Redis)

## 监控和日志

### 配置日志
修改 `app/main.py` 添加日志配置:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### 监控工具推荐
- **Prometheus**: 指标收集
- **Grafana**: 数据可视化
- **Sentry**: 错误追踪

## 常见问题

### 1. 端口被占用
```bash
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000

# 杀死进程
kill -9 <PID>
```

### 2. 权限问题
```bash
# Linux/Mac
chmod -R 755 uploads/
chown -R www-data:www-data /path/to/panpan-studio
```

### 3. 依赖安装失败
```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
npm install --registry=https://registry.npmmirror.com
```

## 安全建议

1. **修改默认密码**: 务必修改管理员默认密码
2. **使用强SECRET_KEY**: 生成随机密钥
3. **启用HTTPS**: 生产环境必须使用SSL
4. **配置防火墙**: 限制访问端口
5. **定期备份**: 设置自动备份任务
6. **更新依赖**: 定期更新依赖包版本

## 更新部署

### 拉取最新代码
```bash
git pull origin main
```

### 更新后端
```bash
pip install -r requirements.txt --upgrade
```

### 更新前端
```bash
cd frontend
npm install
npm run build
cp -r dist/* ../app/static/
```

### 重启服务
```bash
# Supervisor
supervisorctl restart panpan-studio

# Docker
docker restart panpan-studio

# 手动
# 停止现有进程后重新启动
python run.py
```

## 技术支持

如遇到问题,请查看:
- API文档: http://localhost:8000/docs
- 项目README: README.md
- API详细文档: README_API.md
