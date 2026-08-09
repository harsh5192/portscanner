import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Port(Base):
    __tablename__ = "ports"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    host_id = Column(String(36), ForeignKey("hosts.id", ondelete="CASCADE"), nullable=False, index=True)
    port_number = Column(Integer, nullable=False, index=True)
    protocol = Column(String(10), nullable=False, default="tcp")  # tcp, udp
    state = Column(String(20), nullable=False, default="open")   # open, closed, filtered
    state_reason = Column(String(100), nullable=True)

    # Relationships
    host = relationship("Host", back_populates="ports")
    service = relationship("Service", uselist=False, back_populates="port", cascade="all, delete-orphan")
    vulnerabilities = relationship("Vulnerability", back_populates="port", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Port(number={self.port_number}, proto='{self.protocol}', state='{self.state}')>"
