import pytz
import time as t

from datetime import datetime, time, timedelta

from apscheduler.schedulers.background import BackgroundScheduler

from carinsurance_api.core.config import Settings
from carinsurance_api.db.models.car import Car
from carinsurance_api.db.models.claim import Claim
from carinsurance_api.db.models.policy import Policy
from carinsurance_api.db.models.owner import Owner
from carinsurance_api.db.session import SessionLocal


configuration = Settings()
job_interval_minutes = configuration.job_interval_minutes
server_tz = configuration.server_tz


def log_policy_expiry():
    tz = pytz.timezone(server_tz)
    now = datetime.now(tz)
    today = now.date()

    db = SessionLocal()

    try:
        policies = db.query(Policy).filter(
            Policy.end_date == today,
            Policy.logged_expiry_at == None
        ).all()

        for policy in policies:
            car = db.get(Car, policy.car_id)
            print(f"Policy expired: {policy.id}, End Date: {policy.end_date}, Policy provider: {policy.provider},"
                  f" Car ID: {policy.car_id}, Car vin: {car.vin}")

            policy.logged_expiry_at = now
            db.commit()

    finally:
        db.close()


if __name__ == "__main__":
    if configuration.scheduler_enabled:
        scheduler = BackgroundScheduler(timezone=server_tz)
        scheduler.add_job(
            log_policy_expiry,
            "interval",
            minutes=job_interval_minutes,
            next_run_time=datetime.now() + timedelta(seconds=5)
        )
        scheduler.start()
        print(f"Scheduled log_policy_expiry every {job_interval_minutes} minutes.")
        try:
            while True:
                t.sleep(60)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
    else:
        print("Scheduler is disabled by configuration.")
