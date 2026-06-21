from fastapi import FastAPI
from app.routers.user import router as user_router
from app.routers.category import (
    router as category_router
)
app = FastAPI(title="E-Commerce Backend")

app.include_router(user_router)
app.include_router(category_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to E-Commerce Backend API"
    }
