from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):

    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    cameras = relationship("Camera", back_populates="owner", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.username}>"


class Camera(Base):
    __tablename__ = "cameras"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    rtsp_url = Column(String, nullable=False)
    location = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    status = Column(String, default="offline")
    last_seen = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    owner = relationship("User", back_populates="cameras")
    known_faces = relationship("KnownFace", back_populates="camera", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="camera", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Camera {self.name} - {self.status}>"


class KnownFace(Base):
    __tablename__ = "known_faces"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    relationship_type = Column(String, nullable=True)
    image_path = Column(String, nullable=False)
    encoding_data = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=False)
    
    camera = relationship("Camera", back_populates="known_faces")
    
    def __repr__(self):
        return f"<KnownFace {self.name}>"


class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String, default="unknown_face")
    confidence = Column(Float, nullable=True)
    image_path = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="pending")
    is_read = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)
    
    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=False)
    
    camera = relationship("Camera", back_populates="alerts")
    
    def __repr__(self):
        return f"<Alert {self.alert_type} - {self.timestamp}>"