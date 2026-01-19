@echo off
chcp 65001
echo ======================================
echo    穿戴甲电商系统启动脚本
echo ======================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python,请先安装Python 3.11+
    pause
    exit /b 1
)

REM 检查Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Node.js,请先安装Node.js 18+
    pause
    exit /b 1
)

REM 安装后端依赖
echo [1/4] 检查后端依赖...
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

REM 安装前端依赖
echo.
echo [2/4] 检查前端依赖...
cd frontend
if not exist "node_modules" (
    echo 安装前端依赖...
    npm install --registry=https://registry.npmmirror.com
)

REM 构建前端
echo.
echo [3/4] 构建前端...
call npm run build

REM 移动构建文件到后端静态目录
cd ..
if exist "app\static" rmdir /s /q app\static
mkdir app\static
xcopy /s /e /y frontend\dist\* app\static\

REM 启动后端服务
echo.
echo [4/4] 启动服务...
echo.
echo ======================================
echo   服务启动成功!
echo   前台地址: http://localhost:8000
echo   后台地址: http://localhost:8000/admin/login
echo   API文档: http://localhost:8000/docs
echo
echo   默认管理员账号:
echo   用户名: admin
echo   密码: admin123
echo ======================================
echo.

python run.py
pause
