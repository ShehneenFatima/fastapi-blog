from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from ..models import BlogPost, BlogPostCreate

router = APIRouter(prefix="/posts", tags=["Blog Posts"])

# In-memory "database"
posts = []
next_id = 1  # To simulate auto-incrementing IDs

# POST /posts
@router.post("/", response_model=BlogPost, status_code=201)
def create_post(post: BlogPostCreate):
    global next_id
    now = datetime.now()
    new_post = {
        "id": next_id,
        "title": post.title,
        "content": post.content,
        "created_at": now,
        "updated_at": None
    }
    posts.append(new_post)
    next_id += 1
    return new_post

# GET /posts
@router.get("/", response_model=List[BlogPost])
def get_all_posts():
    return posts

# GET /posts/{index}
@router.get("/{post_id}", response_model=BlogPost)
def get_post(post_id: int):
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")

# PUT /posts/{post_id}
@router.put("/{post_id}", response_model=BlogPost)
def update_post(post_id: int, updated_post: BlogPostCreate):
    for post in posts:
        if post["id"] == post_id:
            post.update({
                "title": updated_post.title,
                "content": updated_post.content,
                "updated_at": datetime.now()
            })
            return post
    raise HTTPException(status_code=404, detail="Post not found")

# DELETE /posts/{post_id}
@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts.pop(index)
            return
    raise HTTPException(status_code=404, detail="Post not found")