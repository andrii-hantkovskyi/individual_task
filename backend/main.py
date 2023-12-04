from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

import settings
from admin.router import admin_router
from database import backup_db
from orders.router import orders_router
from products.router import products_router
from users.auth import BearerTokenAuthBackend
from users.router import users_router
from users.services import reset_all_login_unsuccessful_attempts

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.add_middleware(AuthenticationMiddleware, backend=BearerTokenAuthBackend())

app.include_router(prefix='/api', router=orders_router)
app.include_router(prefix='/api', router=products_router)
app.include_router(prefix='/api', router=users_router)
app.include_router(prefix='/api', router=admin_router)


@app.on_event('startup')
async def init_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.timezone = settings.TZ

    scheduler.add_job(reset_all_login_unsuccessful_attempts, 'cron', day='*')
    scheduler.add_job(backup_db, 'cron', day='*', hour=18)

    scheduler.start()
