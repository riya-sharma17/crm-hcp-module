from sqlalchemy import Column, Integer, String, DateTime, Text, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class HCPSpecialty(str, enum.Enum):
    CARDIOLOGIST = "Cardiologist"
    ONCOLOGIST = "Oncologist"
    NEUROLOGIST = "Neurologist"
    GENERAL_PHYSICIAN = "General Physician"
    PEDIATRICIAN = "Pediatrician"
    DERMATOLOGIST = "Dermatologist"
    PSYCHIATRIST = "Psychiatrist"
    ORTHOPEDIC = "Orthopedic"
    OTHER = "Other"

class HCP(Base):
    __tablename__ = "hcps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    specialty = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    phone = Column(String(20), nullable=True)
    hospital = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<HCP {self.name} - {self.specialty}>"