import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Host(Base):
    __tablename__ = "hosts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    scan_id = Column(String(36), ForeignKey("scans.id", ondelete="CASCADE"), nullable=False, index=True)
    ip_address = Column(String(45), nullable=False, index=True)
    hostname = Column(String(255), nullable=True)
    mac_address = Column(String(17), nullable=True)
    status = Column(String(20), nullable=False, default="up")  # up, down, unknown
    os_match = Column(String(255), nullable=True)

    # Relationships
    scan = relationship("Scan", back_populates="hosts")
    ports = relationship("Port", back_populates="host", cascade="all, delete-orphan")
    vulnerabilities = relationship("Vulnerability", back_populates="host", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Host(ip='{self.ip_address}', hostname='{self.hostname}', status='{self.status}')>"
