from sqlalchemy.orm import Session
from app.models.database import Message, User
from typing import List
from sqlalchemy import or_, and_

def send_message(db: Session, sender_id: int, receiver_id: int, content: str):
    """Send a message from one user to another."""
    message = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def get_conversation(db: Session, user1_id: int, user2_id: int, limit: int = 50):
    """Get conversation between two users."""
    return db.query(Message).filter(
        or_(
            and_(Message.sender_id == user1_id, Message.receiver_id == user2_id),
            and_(Message.sender_id == user2_id, Message.receiver_id == user1_id)
        )
    ).order_by(Message.created_at.asc()).limit(limit).all()

def mark_messages_as_read(db: Session, user_id: int, sender_id: int):
    """Mark all messages from sender to user as read."""
    messages = db.query(Message).filter(
        Message.sender_id == sender_id,
        Message.receiver_id == user_id,
        Message.read == False
    ).all()
    
    for message in messages:
        message.read = True
    
    db.commit()
    return len(messages)

def get_unread_messages_count(db: Session, user_id: int):
    """Get count of unread messages for a user."""
    return db.query(Message).filter(
        Message.receiver_id == user_id,
        Message.read == False
    ).count()

def get_conversations(db: Session, user_id: int):
    """Get all conversations for a user."""
    # Get all users this user has exchanged messages with
    sent_to = db.query(Message.receiver_id).filter(Message.sender_id == user_id).distinct().all()
    received_from = db.query(Message.sender_id).filter(Message.receiver_id == user_id).distinct().all()
    
    # Combine and remove duplicates
    user_ids = set([id[0] for id in sent_to] + [id[0] for id in received_from])
    
    # Get user objects
    users = db.query(User).filter(User.id.in_(user_ids)).all()
    
    # Get last message and unread count for each conversation
    conversations = []
    for other_user in users:
        last_message = db.query(Message).filter(
            or_(
                and_(Message.sender_id == user_id, Message.receiver_id == other_user.id),
                and_(Message.sender_id == other_user.id, Message.receiver_id == user_id)
            )
        ).order_by(Message.created_at.desc()).first()
        
        unread_count = db.query(Message).filter(
            Message.sender_id == other_user.id,
            Message.receiver_id == user_id,
            Message.read == False
        ).count()
        
        conversations.append({
            "user": other_user,
            "last_message": last_message,
            "unread_count": unread_count
        })
    
    # Sort by last message time
    conversations.sort(key=lambda x: x["last_message"].created_at if x["last_message"] else None, reverse=True)
    
    return conversations