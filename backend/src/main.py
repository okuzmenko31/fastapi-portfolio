from fastapi import FastAPI

from src.auth.api import router as auth_router

routers = [auth_router]

app = FastAPI(
    title='Portfolio'
)

for router in routers:
    app.include_router(router)
