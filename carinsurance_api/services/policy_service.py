from carinsurance_api.api.schemas import PolicySchema
from carinsurance_api.db.models.policy import Policy

from datetime import date

from sqlalchemy.orm import Session

from typing import List


def create_policy(db: Session, policy_data: PolicySchema) -> Policy:
    policy = Policy(**policy_data.model_dump())
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy


def update_policy(db: Session, policy_id: int, policy_data: PolicySchema) -> Policy:
    policy = db.get(Policy, policy_id)
    if not policy:
        raise ValueError("Policy not found")
    for key, value in policy_data.model_dump().items():
        setattr(policy, key, value)
    db.commit()
    db.refresh(policy)
    return policy


def get_active_policies_by_date(db: Session, car_id: int, target_date: date) -> List[Policy] | None:
    return db.query(Policy).filter(
        Policy.car_id == car_id,
        Policy.start_date <= target_date,
        Policy.end_date >= target_date
    ).all()
