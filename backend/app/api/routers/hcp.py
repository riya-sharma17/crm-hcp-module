from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import List, Optional
import logging

from app.core.database import get_db
from app.core.exceptions import (
    HCPNotFoundException,
    DatabaseException,
    ValidationException
)
from app.models.hcp import HCP
from app.schemas.hcp import HCPCreate, HCPUpdate, HCPResponse

router = APIRouter(prefix="/api/hcp", tags=["HCP"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=HCPResponse)
def create_hcp(hcp: HCPCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating HCP: {hcp.name}")
    try:
        db_hcp = HCP(**hcp.model_dump())
        db.add(db_hcp)
        db.commit()
        db.refresh(db_hcp)
        logger.info(f"HCP created: ID {db_hcp.id}")
        return db_hcp
    except IntegrityError:
        db.rollback()
        raise ValidationException(
            f"HCP with email {hcp.email} already exists"
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"DB error creating HCP: {str(e)}")
        raise DatabaseException(str(e))


@router.get("/", response_model=List[HCPResponse])
def get_all_hcps(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    try:
        return db.query(HCP).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"DB error fetching HCPs: {str(e)}")
        raise DatabaseException(str(e))


@router.get("/search", response_model=List[HCPResponse])
def search_hcps(
    name: Optional[str] = Query(None),
    specialty: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    try:
        query = db.query(HCP)
        if name:
            query = query.filter(HCP.name.ilike(f"%{name}%"))
        if specialty:
            query = query.filter(
                HCP.specialty.ilike(f"%{specialty}%")
            )
        if city:
            query = query.filter(HCP.city.ilike(f"%{city}%"))
        return query.limit(20).all()
    except SQLAlchemyError as e:
        logger.error(f"DB error searching HCPs: {str(e)}")
        raise DatabaseException(str(e))


@router.get("/{hcp_id}", response_model=HCPResponse)
def get_hcp(hcp_id: int, db: Session = Depends(get_db)):
    try:
        hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
        if not hcp:
            raise HCPNotFoundException(hcp_id=hcp_id)
        return hcp
    except HCPNotFoundException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"DB error fetching HCP: {str(e)}")
        raise DatabaseException(str(e))


@router.put("/{hcp_id}", response_model=HCPResponse)
def update_hcp(
    hcp_id: int,
    hcp_update: HCPUpdate,
    db: Session = Depends(get_db)
):
    try:
        hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
        if not hcp:
            raise HCPNotFoundException(hcp_id=hcp_id)
        update_data = hcp_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(hcp, field, value)
        db.commit()
        db.refresh(hcp)
        logger.info(f"HCP updated: ID {hcp_id}")
        return hcp
    except HCPNotFoundException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"DB error updating HCP: {str(e)}")
        raise DatabaseException(str(e))


@router.delete("/{hcp_id}")
def delete_hcp(hcp_id: int, db: Session = Depends(get_db)):
    try:
        hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
        if not hcp:
            raise HCPNotFoundException(hcp_id=hcp_id)
        db.delete(hcp)
        db.commit()
        logger.info(f"HCP deleted: ID {hcp_id}")
        return {"success": True, "message": "HCP deleted successfully"}
    except HCPNotFoundException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"DB error deleting HCP: {str(e)}")
        raise DatabaseException(str(e))