from fastapi import Depends
from fastapi import FastAPI
from app.core.security import hash_password
from app.core.security import verify_password
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.routers.user import router as user_router

app = FastAPI(title="E-Commerce Backend")
 
app.include_router(user_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to E-Commerce Backend API"
    }