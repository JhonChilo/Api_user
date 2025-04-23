from fastapi import FastAPI
from app.auth.controllers.user_controller import router as user_router

app = FastAPI()

app.include_router(user_router, prefix="/api/v1", tags=["users"])