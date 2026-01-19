from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from app.database import init_db, get_db, async_session_maker
from app.config import settings
from app.models.user import User
from app.utils.security import get_password_hash
from app.api import products, cart, orders
from app.api.admin import auth, products as admin_products, orders as admin_orders

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化数据库
    await init_db()

    # 创建默认管理员账号
    async with async_session_maker() as db:
        result = await db.execute(select(User).where(User.username == settings.ADMIN_USERNAME))
        admin = result.scalar_one_or_none()

        if not admin:
            admin = User(
                username=settings.ADMIN_USERNAME,
                hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
                is_admin=True
            )
            db.add(admin)
            await db.commit()
            print(f"已创建默认管理员账号: {settings.ADMIN_USERNAME}")

    # 创建上传目录
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    Path(settings.UPLOAD_DIR + "/products").mkdir(parents=True, exist_ok=True)
    Path(settings.UPLOAD_DIR + "/payment").mkdir(parents=True, exist_ok=True)

    yield

app = FastAPI(
    title="穿戴甲电商系统",
    description="穿戴甲(美甲)销售的轻量级电商平台",
    version="1.0.0",
    lifespan=lifespan
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API路由
app.include_router(products.router, prefix="/api")
app.include_router(cart.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(admin_products.router, prefix="/api")
app.include_router(admin_orders.router, prefix="/api")

@app.get("/health")
async def health():
    return {"status": "healthy"}

# 静态文件服务
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# 前端静态文件服务 (放在最后)
static_path = Path("app/static")
if static_path.exists():
    app.mount("/assets", StaticFiles(directory="app/static/assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = Path("app/static") / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse("app/static/index.html")
