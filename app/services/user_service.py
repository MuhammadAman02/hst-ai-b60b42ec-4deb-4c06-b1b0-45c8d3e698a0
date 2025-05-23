from sqlalchemy.orm import Session
from app.models.database import User, Experience, Education, ConnectionRequest
from app.services.auth import get_password_hash
from typing import List, Optional
from datetime import datetime
import os
import shutil
from fastapi import UploadFile

def create_user(db: Session, email: str, username: str, password: str, full_name: str):
    """Create a new user."""
    hashed_password = get_password_hash(password)
    db_user = User(
        email=email,
        username=username,
        hashed_password=hashed_password,
        full_name=full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    """Get a user by username."""
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    """Get a user by email."""
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    """Get a user by ID."""
    return db.query(User).filter(User.id == user_id).first()

def update_profile(db: Session, user_id: int, **kwargs):
    """Update user profile."""
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    for key, value in kwargs.items():
        if hasattr(user, key) and key != "id" and key != "hashed_password":
            setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

def update_profile_image(db: Session, user_id: int, file: UploadFile):
    """Update user profile image."""
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    # Create directory if it doesn't exist
    upload_dir = "app/static/profile_images"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file
    file_path = f"{upload_dir}/{user_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update user profile image path
    relative_path = f"/static/profile_images/{user_id}_{file.filename}"
    user.profile_image = relative_path
    db.commit()
    db.refresh(user)
    return user

def add_experience(db: Session, user_id: int, title: str, company: str, 
                  location: Optional[str], start_date: datetime, 
                  end_date: Optional[datetime], current: bool, 
                  description: Optional[str]):
    """Add a new experience to user profile."""
    experience = Experience(
        user_id=user_id,
        title=title,
        company=company,
        location=location,
        start_date=start_date,
        end_date=end_date,
        current=current,
        description=description
    )
    db.add(experience)
    db.commit()
    db.refresh(experience)
    return experience

def add_education(db: Session, user_id: int, school: str, degree: str, 
                 field_of_study: Optional[str], start_date: datetime, 
                 end_date: Optional[datetime], current: bool, 
                 description: Optional[str]):
    """Add a new education to user profile."""
    education = Education(
        user_id=user_id,
        school=school,
        degree=degree,
        field_of_study=field_of_study,
        start_date=start_date,
        end_date=end_date,
        current=current,
        description=description
    )
    db.add(education)
    db.commit()
    db.refresh(education)
    return education

def get_user_connections(db: Session, user_id: int):
    """Get all connections for a user."""
    user = get_user_by_id(db, user_id)
    if not user:
        return []
    return user.connections

def send_connection_request(db: Session, sender_id: int, receiver_id: int):
    """Send a connection request."""
    # Check if request already exists
    existing_request = db.query(ConnectionRequest).filter(
        ConnectionRequest.sender_id == sender_id,
        ConnectionRequest.receiver_id == receiver_id,
        ConnectionRequest.status == "pending"
    ).first()
    
    if existing_request:
        return existing_request
    
    # Check if users are already connected
    sender = get_user_by_id(db, sender_id)
    if any(conn.id == receiver_id for conn in sender.connections):
        return None
    
    # Create new request
    request = ConnectionRequest(
        sender_id=sender_id,
        receiver_id=receiver_id
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request

def accept_connection_request(db: Session, request_id: int):
    """Accept a connection request."""
    request = db.query(ConnectionRequest).filter(ConnectionRequest.id == request_id).first()
    if not request or request.status != "pending":
        return None
    
    # Update request status
    request.status = "accepted"
    
    # Add connection to both users
    sender = get_user_by_id(db, request.sender_id)
    receiver = get_user_by_id(db, request.receiver_id)
    
    sender.connections.append(receiver)
    
    db.commit()
    return request

def reject_connection_request(db: Session, request_id: int):
    """Reject a connection request."""
    request = db.query(ConnectionRequest).filter(ConnectionRequest.id == request_id).first()
    if not request or request.status != "pending":
        return None
    
    request.status = "rejected"
    db.commit()
    return request

def get_pending_requests(db: Session, user_id: int):
    """Get pending connection requests for a user."""
    return db.query(ConnectionRequest).filter(
        ConnectionRequest.receiver_id == user_id,
        ConnectionRequest.status == "pending"
    ).all()

def search_users(db: Session, query: str, limit: int = 10):
    """Search for users by name or headline."""
    return db.query(User).filter(
        (User.full_name.ilike(f"%{query}%")) | 
        (User.headline.ilike(f"%{query}%")) |
        (User.username.ilike(f"%{query}%"))
    ).limit(limit).all()