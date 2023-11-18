from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import settings
from orders.router import orders_router
from products.router import products_router
from users.router import users_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(prefix='/api', router=orders_router)
app.include_router(prefix='/api', router=products_router)
app.include_router(prefix='/api', router=users_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
