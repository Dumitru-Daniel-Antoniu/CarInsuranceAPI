from carinsurance_api.api.schemas import ClaimSchema
from carinsurance_api.db.models.claim import Claim

from sqlalchemy.orm import Session


def create_claim(db: Session, claim_data: ClaimSchema) -> tuple[Claim, str]:
    claim = Claim(**claim_data.model_dump())
    db.add(claim)
    db.commit()
    db.refresh(claim)
    location = f"/api/cars/{claim.car_id}/claims/{claim.id}"
    return claim, location
