from carinsurance_api.db.models.car import Car
from carinsurance_api.services.policy_service import get_active_policies_by_date

from sqlalchemy.orm import Session


def valid_car_and_policy(db: Session, car_id: int, target_date: date) -> bool:
    car = db.get(Car, car_id)
    if not car:
        return False
    policy = get_active_policies_by_date(db, car_id, target_date)
    return policy is not None
