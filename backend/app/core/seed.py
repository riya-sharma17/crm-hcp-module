import logging
from sqlalchemy.orm import Session
from app.models.hcp import HCP

logger = logging.getLogger(__name__)

SAMPLE_HCPS = [
    {
        "name": "Dr. Rahul Sharma",
        "specialty": "Cardiologist",
        "hospital": "AIIMS Delhi",
        "city": "Delhi",
        "phone": "+91-9876543210",
        "email": "rahul.sharma@aiims.edu"
    },
    {
        "name": "Dr. Priya Patel",
        "specialty": "Oncologist",
        "hospital": "Tata Memorial Hospital",
        "city": "Mumbai",
        "phone": "+91-9876543211",
        "email": "priya.patel@tmc.gov.in"
    },
    {
        "name": "Dr. Amit Kumar",
        "specialty": "Neurologist",
        "hospital": "Apollo Hospital",
        "city": "Bangalore",
        "phone": "+91-9876543212",
        "email": "amit.kumar@apollo.com"
    },
    {
        "name": "Dr. Sneha Singh",
        "specialty": "General Physician",
        "hospital": "Fortis Hospital",
        "city": "Delhi",
        "phone": "+91-9876543213",
        "email": "sneha.singh@fortis.com"
    },
    {
        "name": "Dr. Smith Johnson",
        "specialty": "Cardiologist",
        "hospital": "City Hospital",
        "city": "Delhi",
        "phone": "+91-9876543214",
        "email": "smith.johnson@cityhospital.com"
    },
    {
        "name": "Dr. Anjali Mehta",
        "specialty": "Dermatologist",
        "hospital": "Skin Care Clinic",
        "city": "Mumbai",
        "phone": "+91-9876543215",
        "email": "anjali.mehta@skincare.com"
    },
    {
        "name": "Dr. Vikram Rao",
        "specialty": "Orthopedic",
        "hospital": "Manipal Hospital",
        "city": "Bangalore",
        "phone": "+91-9876543216",
        "email": "vikram.rao@manipal.com"
    },
    {
        "name": "Dr. Kavita Reddy",
        "specialty": "Pediatrician",
        "hospital": "Rainbow Hospital",
        "city": "Hyderabad",
        "phone": "+91-9876543217",
        "email": "kavita.reddy@rainbow.com"
    },
]


def seed_hcps(db: Session):
    """Seed HCPs only if table is empty"""
    existing = db.query(HCP).count()
    if existing > 0:
        logger.info(f"HCPs already seeded ({existing} records)")
        return

    for hcp_data in SAMPLE_HCPS:
        hcp = HCP(**hcp_data)
        db.add(hcp)

    db.commit()
    logger.info(f"Seeded {len(SAMPLE_HCPS)} HCPs successfully")