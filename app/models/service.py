import uuid
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    port_id = Column(String(36), ForeignKey("ports.id", ondelete="CASCADE"), nullable=False, unique=True)
    name = Column(String(100), nullable=True, default="unknown")
    product = Column(String(255), nullable=True)
    version = Column(String(255), nullable=True)
    extra_info = Column(Text, nullable=True)
    hostname = Column(String(255), nullable=True)
    ostype = Column(String(100), nullable=True)
    cpe = Column(String(255), nullable=True)

    # Relationships
    port = relationship("Port", back_populates="service")

    def __repr__(self):
        return f"<Service(name='{self.name}', product='{self.product}', version='{self.version}')>"
