import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.orm import relationship
from app.models.base import Base

class Scan(Base):
    __tablename__ = "scans"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    target = Column(String(255), nullable=False, index=True)
    scan_type = Column(String(50), nullable=False, default="DEFAULT")
    scanner = Column(String(50), nullable=False, default="nmap")
    command_options = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="PENDING")  # PENDING, RUNNING, COMPLETED, FAILED
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_time = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)

    # Relationships
    hosts = relationship("Host", back_populates="scan", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Scan(id={self.id}, target='{self.target}', status='{self.status}')>"
