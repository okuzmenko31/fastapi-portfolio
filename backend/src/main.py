from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.api import router as auth_router
from src.portfolio_info.api import router as info_router

origins = ['http://localhost:3000']

routers = [auth_router, info_router]

app = FastAPI(
    title='Portfolio'
)

for router in routers:
    app.include_router(router, prefix='/api/v1')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
