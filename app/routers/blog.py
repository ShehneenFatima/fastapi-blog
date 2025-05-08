from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime

# Import models and auth dependency
from ..models import BlogPost, BlogPostCreate
from ..auth import get_current_active_user

# Create router with prefix and tag
router = APIRouter(
    prefix="/posts",
    tags=["Blog Posts"],
    dependencies=[Depends(get_current_active_user)]  # Protect all routes in this router
)

# In-memory "database"
posts = []
next_id = 1  # Simulates auto-incrementing ID

# POST /posts
@router.post("/", response_model=BlogPost, status_code=201)
def create_post(post: BlogPostCreate):
    """
    Create a new blog post.
    Requires valid JWT token.
    """
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
    """
    Get a list of all blog posts.
    Requires valid JWT token.
    """
    return posts


# GET /posts/{post_id}
@router.get("/{post_id}", response_model=BlogPost)
def get_post(post_id: int):
    """
    Get a single blog post by ID.
    Requires valid JWT token.
    """
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")


# PUT /posts/{post_id}
@router.put("/{post_id}", response_model=BlogPost)
def update_post(post_id: int, updated_post: BlogPostCreate):
    """
    Update an existing blog post.
    Requires valid JWT token.
    """
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
    """
    Delete a blog post by ID.
    Requires valid JWT token.
    """
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts.pop(index)
            return
    raise HTTPException(status_code=404, detail="Post not found")