from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.models.interaction import Interaction
from app.models.hcp import HCP
from app.schemas.interaction import (
    InteractionCreate,
    InteractionUpdate,
    InteractionResponse
)

router = APIRouter(prefix="/api/interactions", tags=["Interactions"])


@router.post("/", response_model=InteractionResponse)
def create_interaction(
    interaction: InteractionCreate,
    db: Session = Depends(get_db)
):
    """Create a new interaction via form"""

    # Check HCP exists
    hcp = db.query(HCP).filter(HCP.id == interaction.hcp_id).first()
    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")

    db_interaction = Interaction(**interaction.model_dump())
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction


@router.get("/", response_model=List[InteractionResponse])
def get_all_interactions(
    skip: int = 0,
    limit: int = 50,
    hcp_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all interactions, optionally filtered by HCP"""
    query = db.query(Interaction)

    if hcp_id:
        query = query.filter(Interaction.hcp_id == hcp_id)

    interactions = query.order_by(
        Interaction.created_at.desc()
    ).offset(skip).limit(limit).all()

    return interactions


@router.get("/{interaction_id}", response_model=InteractionResponse)
def get_interaction(
    interaction_id: int,
    db: Session = Depends(get_db)
):
    """Get a single interaction by ID"""
    interaction = db.query(Interaction).filter(
        Interaction.id == interaction_id
    ).first()

    if not interaction:
        raise HTTPException(
            status_code=404,
            detail="Interaction not found"
        )
    return interaction


@router.put("/{interaction_id}", response_model=InteractionResponse)
def update_interaction(
    interaction_id: int,
    interaction_update: InteractionUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing interaction"""
    interaction = db.query(Interaction).filter(
        Interaction.id == interaction_id
    ).first()

    if not interaction:
        raise HTTPException(
            status_code=404,
            detail="Interaction not found"
        )

    update_data = interaction_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(interaction, field, value)

    interaction.is_edited = True
    interaction.updated_at = datetime.now()

    db.commit()
    db.refresh(interaction)
    return interaction


@router.delete("/{interaction_id}")
def delete_interaction(
    interaction_id: int,
    db: Session = Depends(get_db)
):
    """Delete an interaction"""
    interaction = db.query(Interaction).filter(
        Interaction.id == interaction_id
    ).first()

    if not interaction:
        raise HTTPException(
            status_code=404,
            detail="Interaction not found"
        )

    db.delete(interaction)
    db.commit()
    return {"message": "Interaction deleted successfully"}