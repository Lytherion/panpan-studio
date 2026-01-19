#!/bin/bash

echo "======================================"
echo "   穿戴甲电商系统启动脚本"
echo "======================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python,请先安装Python 3.11+"
    exit 1
fi

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "[错误] 未检测到Node.js,请先安装Node.js 18+"
    exit 1
fi

# 安装后端依赖
echo "[1/4] 检查后端依赖..."
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 安装前端依赖
echo ""
echo "[2/4] 检查前端依赖..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install --registry=https://registry.npmmirror.com
fi

# 构建前端
echo ""
echo "[3/4] 构建前端..."
npm run build

# 移动构建文件到后端静态目录
cd ..
rm -rf app/static
mkdir -p app/static
cp -r frontend/dist/* app/static/

# 启动后端服务
echo ""
echo "[4/4] 启动服务..."
echo ""
echo "======================================"
echo "  服务启动成功!"
echo "  前台地址: http://localhost:8000"
echo "  后台地址: http://localhost:8000/admin/login"
echo "  API文档: http://localhost:8000/docs"
echo "  "
echo "  默认管理员账号:"
echo "  用户名: admin"
echo "  密码: admin123"
echo "======================================"
echo ""

python3 run.py
