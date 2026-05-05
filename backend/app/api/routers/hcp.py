from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.hcp import HCP
from app.schemas.hcp import HCPCreate, HCPUpdate, HCPResponse

router = APIRouter(prefix="/api/hcp", tags=["HCP"])


@router.post("/", response_model=HCPResponse)
def create_hcp(hcp: HCPCreate, db: Session = Depends(get_db)):
    """Create a new HCP"""
    db_hcp = HCP(**hcp.model_dump())
    db.add(db_hcp)
    db.commit()
    db.refresh(db_hcp)
    return db_hcp


@router.get("/", response_model=List[HCPResponse])
def get_all_hcps(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all HCPs"""
    hcps = db.query(HCP).offset(skip).limit(limit).all()
    return hcps


@router.get("/search", response_model=List[HCPResponse])
def search_hcps(
    name: Optional[str] = Query(None),
    specialty: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Search HCPs by name, specialty or city"""
    query = db.query(HCP)

    if name:
        query = query.filter(HCP.name.ilike(f"%{name}%"))
    if specialty:
        query = query.filter(HCP.specialty.ilike(f"%{specialty}%"))
    if city:
        query = query.filter(HCP.city.ilike(f"%{city}%"))

    return query.limit(20).all()


@router.get("/{hcp_id}", response_model=HCPResponse)
def get_hcp(hcp_id: int, db: Session = Depends(get_db)):
    """Get a single HCP by ID"""
    hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")
    return hcp


@router.put("/{hcp_id}", response_model=HCPResponse)
def update_hcp(
    hcp_id: int,
    hcp_update: HCPUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing HCP"""
    hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")

    update_data = hcp_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(hcp, field, value)

    db.commit()
    db.refresh(hcp)
    return hcp


@router.delete("/{hcp_id}")
def delete_hcp(hcp_id: int, db: Session = Depends(get_db)):
    """Delete an HCP"""
    hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")

    db.delete(hcp)
    db.commit()
    return {"message": "HCP deleted successfully"}