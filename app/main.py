from fastapi import FastAPI
from app.routers import blog, auth  
from fastapi import FastAPI
from app.auth import pwd_context

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI Blog API"}

app.include_router(blog.router)
app.include_router(auth.router)  



@app.get("/test-password")
def test_password():
    hashed = "$2b$12$EixZaYVK1fsbw1ZfbX3NXeKWLW9rhxwH8lK9khznyG6TsgOKLdO/."  # 'secret'
    result = pwd_context.verify("secret", hashed)
    return {"match": result}