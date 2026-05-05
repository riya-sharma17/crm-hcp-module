from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Schema for CREATING interaction via FORM
class InteractionCreate(BaseModel):
    hcp_id: int
    hcp_name: str
    interaction_type: str = "Meeting"
    interaction_date: datetime
    attendees: Optional[List[str]] = []
    topics_discussed: Optional[str] = None
    materials_shared: Optional[List[dict]] = []
    samples_distributed: Optional[List[dict]] = []
    sentiment: Optional[str] = "Neutral"
    outcomes: Optional[str] = None
    follow_up_actions: Optional[List[str]] = []
    logged_via: Optional[str] = "form"
    raw_chat_input: Optional[str] = None


# Schema for CREATING interaction via CHAT
class InteractionChatCreate(BaseModel):
    message: str          # Raw chat message from user
    hcp_id: Optional[int] = None


# Schema for UPDATING interaction
class InteractionUpdate(BaseModel):
    interaction_type: Optional[str] = None
    interaction_date: Optional[datetime] = None
    attendees: Optional[List[str]] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[List[dict]] = None
    samples_distributed: Optional[List[dict]] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    follow_up_actions: Optional[List[str]] = None


# Schema for RETURNING interaction data
class InteractionResponse(BaseModel):
    id: int
    hcp_id: int
    hcp_name: str
    interaction_type: str
    interaction_date: datetime
    attendees: Optional[List[str]] = []
    topics_discussed: Optional[str] = None
    materials_shared: Optional[List[dict]] = []
    samples_distributed: Optional[List[dict]] = []
    ai_summary: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    follow_up_actions: Optional[List[str]] = []
    ai_suggested_followups: Optional[List[str]] = []
    logged_via: str
    is_edited: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Schema for CHAT response
class AgentChatResponse(BaseModel):
    message: str
    interaction: Optional[InteractionResponse] = None
    suggested_followups: Optional[List[str]] = []