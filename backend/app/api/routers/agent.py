from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.interaction import InteractionChatCreate, AgentChatResponse
from app.agent.graph import run_agent
from app.models.interaction import Interaction
from app.models.hcp import HCP
from datetime import datetime

router = APIRouter(prefix="/api/agent", tags=["Agent"])


@router.post("/chat", response_model=AgentChatResponse)
async def chat_with_agent(
    chat_input: InteractionChatCreate,
    db: Session = Depends(get_db)
):
    """Send a message to the AI agent"""
    try:
        result = await run_agent(
            message=chat_input.message,
            conversation_history=[]
        )

        # If agent logged an interaction, save it to DB
        tool_results = result.get("tool_results", {})
        saved_interaction = None

        if "log_interaction" in tool_results:
            data = tool_results["log_interaction"]

            # Find HCP
            hcp = db.query(HCP).filter(
                HCP.name.ilike(f"%{data.get('hcp_name', '')}%")
            ).first()

            if hcp:
                interaction = Interaction(
                    hcp_id=hcp.id,
                    hcp_name=hcp.name,
                    interaction_type=data.get(
                        "interaction_type", "Meeting"
                    ),
                    interaction_date=datetime.now(),
                    topics_discussed=data.get("topics_discussed"),
                    sentiment=data.get("sentiment", "Neutral"),
                    outcomes=data.get("outcomes"),
                    follow_up_actions=data.get("follow_up_actions", []),
                    logged_via="chat",
                    raw_chat_input=chat_input.message
                )
                db.add(interaction)
                db.commit()
                db.refresh(interaction)
                saved_interaction = interaction

        return AgentChatResponse(
            message=result["response"],
            interaction=saved_interaction,
            suggested_followups=result.get(
                "tool_results", {}
            ).get("suggest_followups", {}).get("followups", [])
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Agent error: {str(e)}"
        )