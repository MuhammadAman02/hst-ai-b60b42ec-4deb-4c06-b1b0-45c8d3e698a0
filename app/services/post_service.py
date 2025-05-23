from sqlalchemy.orm import Session
from app.models.database import Post, Comment, Like, User
from typing import List, Optional
import os
import shutil
from fastapi import UploadFile
from datetime import datetime

def create_post(db: Session, author_id: int, content: str, image: Optional[UploadFile] = None):
    """Create a new post."""
    image_url = None
    
    # Handle image upload if provided
    if image:
        upload_dir = "app/static/post_images"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = f"{upload_dir}/{author_id}_{datetime.utcnow().timestamp()}_{image.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        image_url = f"/static/post_images/{author_id}_{datetime.utcnow().timestamp()}_{image.filename}"
    
    # Create post
    post = Post(
        author_id=author_id,
        content=content,
        image_url=image_url
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_post_by_id(db: Session, post_id: int):
    """Get a post by ID."""
    return db.query(Post).filter(Post.id == post_id).first()

def get_user_posts(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    """Get posts by a specific user."""
    return db.query(Post).filter(Post.author_id == user_id).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()

def get_feed_posts(db: Session, user_id: int, skip: int = 0, limit: int = 20):
    """Get posts for user's feed (own posts + connections' posts)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return []
    
    # Get IDs of all connections
    connection_ids = [conn.id for conn in user.connections]
    connection_ids.append(user_id)  # Include user's own posts
    
    # Get posts from user and connections
    return db.query(Post).filter(Post.author_id.in_(connection_ids)).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()

def add_comment(db: Session, post_id: int, author_id: int, content: str):
    """Add a comment to a post."""
    comment = Comment(
        post_id=post_id,
        author_id=author_id,
        content=content
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def get_post_comments(db: Session, post_id: int):
    """Get all comments for a post."""
    return db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at.asc()).all()

def like_post(db: Session, post_id: int, user_id: int):
    """Like a post."""
    # Check if already liked
    existing_like = db.query(Like).filter(Like.post_id == post_id, Like.user_id == user_id).first()
    if existing_like:
        return existing_like
    
    # Create new like
    like = Like(
        post_id=post_id,
        user_id=user_id
    )
    db.add(like)
    db.commit()
    db.refresh(like)
    return like

def unlike_post(db: Session, post_id: int, user_id: int):
    """Unlike a post."""
    like = db.query(Like).filter(Like.post_id == post_id, Like.user_id == user_id).first()
    if like:
        db.delete(like)
        db.commit()
        return True
    return False

def has_liked_post(db: Session, post_id: int, user_id: int):
    """Check if a user has liked a post."""
    return db.query(Like).filter(Like.post_id == post_id, Like.user_id == user_id).first() is not None

def get_post_likes_count(db: Session, post_id: int):
    """Get the number of likes for a post."""
    return db.query(Like).filter(Like.post_id == post_id).count()