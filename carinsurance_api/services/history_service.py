from sqlalchemy.orm import Session

from carinsurance_api.db.models.claim import Claim
from carinsurance_api.db.models.policy import Policy


def get_car_history(db: Session, car_id: int) -> list[dict]:
    policies = db.query(Policy).filter(Policy.car_id == car_id).all()
    claims = db.query(Claim).filter(Claim.car_id == car_id).all()

    history = []

    for policy in policies:
        history.append({
            "type": "policy",
            "policyId": policy.id,
            "startDate": policy.start_date.isoformat(),
            "endDate": policy.end_date.isoformat(),
            "provider": policy.provider
        })

    for claim in claims:
        history.append({
            "type": "CLAIM",
            "claimId": claim.id,
            "claimDate": claim.claim_date.isoformat(),
            "amount": claim.amount,
            "description": claim.description
        })

    history.sort(key=lambda x: x.get("startDate") or x.get("claimDate"))
    return history
