from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.core.database import get_db
from app.core.exceptions import (
    AgentException,
    DatabaseException,
    GroqAPIException,
    HCPNotFoundException
)
from app.schemas.interaction import InteractionChatCreate, AgentChatResponse
from app.agent.graph import run_agent
from app.models.interaction import Interaction
from app.models.hcp import HCP
from datetime import datetime

router = APIRouter(prefix="/api/agent", tags=["Agent"])
logger = logging.getLogger(__name__)


@router.post("/chat", response_model=AgentChatResponse)
async def chat_with_agent(
    chat_input: InteractionChatCreate,
    db: Session = Depends(get_db)
):
    logger.info(f"Chat request received: {chat_input.message[:50]}...")

    # Step 1 — Run AI agent
    try:
        result = await run_agent(
            message=chat_input.message,
            conversation_history=[]
        )
        logger.info("Agent ran successfully")
    except Exception as e:
        logger.error(f"Groq/Agent error: {str(e)}")
        raise GroqAPIException(str(e))

    # Step 2 — Extract data
    extracted = result.get("interaction_data", {})
    saved_interaction = None
    logger.info(f"Extracted data: {extracted}")

    # Step 3 — Find HCP
    hcp = None
    if extracted.get("hcp_name"):
        try:
            hcp = db.query(HCP).filter(
                HCP.name.ilike(f"%{extracted['hcp_name']}%")
            ).first()
            if hcp:
                logger.info(f"HCP found: {hcp.name}")
            else:
                logger.warning(
                    f"HCP not found: {extracted['hcp_name']}"
                )
        except SQLAlchemyError as e:
            logger.error(f"Database error finding HCP: {str(e)}")
            raise DatabaseException(str(e))

    # Step 4 — Save interaction if HCP found
    if hcp:
        try:
            interaction = Interaction(
                hcp_id=hcp.id,
                hcp_name=hcp.name,
                interaction_type=extracted.get(
                    "interaction_type", "Meeting"
                ),
                interaction_date=datetime.now(),
                topics_discussed=extracted.get("topics_discussed"),
                sentiment=extracted.get("sentiment", "Neutral"),
                outcomes=extracted.get("outcomes"),
                follow_up_actions=extracted.get(
                    "follow_up_actions", []
                ),
                materials_shared=extracted.get(
                    "materials_shared", []
                ),
                samples_distributed=extracted.get(
                    "samples_distributed", []
                ),
                logged_via="chat",
                raw_chat_input=chat_input.message
            )
            db.add(interaction)
            db.commit()
            db.refresh(interaction)
            saved_interaction = interaction
            logger.info(
                f"Interaction saved: ID {interaction.id}"
            )
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(
                f"Database error saving interaction: {str(e)}"
            )
            raise DatabaseException(str(e))

    return AgentChatResponse(
        message=result["response"],
        interaction=saved_interaction,
        extracted_form_data=extracted,
        suggested_followups=extracted.get("follow_up_actions", [])
    )