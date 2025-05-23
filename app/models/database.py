from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Table, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os

# Create SQLite database engine
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./linkedin_clone.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Connection association table (for many-to-many relationship)
connections = Table(
    'connections',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('connection_id', Integer, ForeignKey('users.id'), primary_key=True)
)

# Connection request table
class ConnectionRequest(Base):
    __tablename__ = "connection_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")  # pending, accepted, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_requests")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_requests")

# User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    headline = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    profile_image = Column(String, nullable=True, default="/static/default_profile.png")
    location = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    experiences = relationship("Experience", back_populates="user", cascade="all, delete-orphan")
    educations = relationship("Education", back_populates="user", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")
    sent_requests = relationship("ConnectionRequest", foreign_keys=[ConnectionRequest.sender_id], back_populates="sender")
    received_requests = relationship("ConnectionRequest", foreign_keys=[ConnectionRequest.receiver_id], back_populates="receiver")
    
    # Many-to-many relationship for connections
    connections = relationship(
        "User",
        secondary=connections,
        primaryjoin=id==connections.c.user_id,
        secondaryjoin=id==connections.c.connection_id,
        backref="connected_to"
    )

# Experience model
class Experience(Base):
    __tablename__ = "experiences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    company = Column(String)
    location = Column(String, nullable=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime, nullable=True)
    current = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    
    user = relationship("User", back_populates="experiences")

# Education model
class Education(Base):
    __tablename__ = "educations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    school = Column(String)
    degree = Column(String)
    field_of_study = Column(String, nullable=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime, nullable=True)
    current = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    
    user = relationship("User", back_populates="educations")

# Post model
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")

# Comment model
class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    post = relationship("Post", back_populates="comments")
    author = relationship("User")

# Like model
class Like(Base):
    __tablename__ = "likes"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    post = relationship("Post", back_populates="likes")
    user = relationship("User")

# Message model
class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")

# Create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()