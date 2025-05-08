from fastapi import FastAPI
from app.routers import blog

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Blog API"}

app.include_router(blog.router)