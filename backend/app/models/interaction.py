from sqlalchemy import (
    Column, Integer, String, DateTime,
    Text, Enum, ForeignKey, JSON, Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class InteractionType(str, enum.Enum):
    MEETING = "Meeting"
    CALL = "Call"
    EMAIL = "Email"
    CONFERENCE = "Conference"
    VIRTUAL = "Virtual"


class SentimentType(str, enum.Enum):
    POSITIVE = "Positive"
    NEUTRAL = "Neutral"
    NEGATIVE = "Negative"


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)

    # HCP Reference
    hcp_id = Column(Integer, ForeignKey("hcps.id"), nullable=False)
    hcp_name = Column(String(255), nullable=False)

    # Interaction Details
    interaction_type = Column(
        String(50),
        default=InteractionType.MEETING
    )
    interaction_date = Column(DateTime(timezone=True), nullable=False)
    attendees = Column(JSON, default=list)

    # Content
    topics_discussed = Column(Text, nullable=True)
    materials_shared = Column(JSON, default=list)
    samples_distributed = Column(JSON, default=list)

    # AI Generated Fields
    ai_summary = Column(Text, nullable=True)
    sentiment = Column(
        String(20),
        default=SentimentType.NEUTRAL
    )
    outcomes = Column(Text, nullable=True)
    follow_up_actions = Column(JSON, default=list)
    ai_suggested_followups = Column(JSON, default=list)

    # Meta
    logged_via = Column(String(20), default="form")  # form or chat
    is_edited = Column(Boolean, default=False)
    raw_chat_input = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    # Relationship
    hcp = relationship("HCP", backref="interactions")

    def __repr__(self):
        return f"<Interaction {self.id} - {self.hcp_name} - {self.interaction_type}>"