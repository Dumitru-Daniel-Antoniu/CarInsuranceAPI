from datetime import datetime

from pydantic import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from carinsurance_api.api.errors import error_response
from carinsurance_api.api.schemas import PolicySchema
from carinsurance_api.core.core_logger import logger
from carinsurance_api.db.models.car import Car
from carinsurance_api.db.models.policy import Policy
from carinsurance_api.db.session import SessionLocal
from carinsurance_api.services.policy_service import create_policy, get_active_policies_by_date
from carinsurance_api.services.validity_service import valid_car_and_policy


class PolicyView(APIView):
    def get(self, request, car_id, policy_id=None):
        db = SessionLocal()

        try:
            if policy_id is not None:
                policy = db.get(Policy, policy_id)

                if not policy or policy.car_id != car_id:
                    return Response(error_response(404, "Policy not found for this car"), status=404)

                response_data = PolicySchema.model_validate(policy).model_dump(by_alias=True)

                return Response(response_data, status=200)

            else:
                car = db.get(Car, car_id)

                if not car:
                    return Response(error_response(404, "Car not found"), status=404)

                policies = db.query(Policy).filter_by(car_id=car_id).all()
                response_data = [PolicySchema.model_validate(policy).model_dump(by_alias=True) for policy in policies]

                return Response(response_data, status=200)

        finally:
            db.close()


    def post(self, request, car_id):
        db = SessionLocal()

        try:
            data = request.data
            data["car_id"] = car_id

            try:
                policy_data = PolicySchema.model_validate(data)
            except ValidationError as ve:
                if ve.errors()[0]['type'] == 'value_error':
                    return Response(error_response(422, "Policy validation error", ve.errors()[0]['msg']), status=422)
                else:
                    return Response(error_response(422, "Policy validation error", ve.errors()), status=422)

            car = db.get(Car, policy_data.car_id)
            if not car:
                return Response(error_response(404, "Car not found"), status=404)

            active_policies_start_date = get_active_policies_by_date(db, car_id, policy_data.start_date)
            active_policies_end_date = get_active_policies_by_date(db, car_id, policy_data.end_date)
            if len(active_policies_start_date) > 0 or len(active_policies_end_date) > 0:
                return Response(error_response(409, "There are policies that overlap"), status=409)

            policy = create_policy(db, policy_data)
            response_data = PolicySchema.model_validate(policy).model_dump(by_alias=True)

            logger.info(
                "Policy created",
                policy_id=policy.id,
                car_id=policy.car_id,
                provider=policy.provider,
                start_date=str(policy.start_date),
                end_date=str(policy.end_date)
            )

            return Response(response_data, status=201)

        finally:
            db.close()


    def delete(self, request, car_id, policy_id):
        db = SessionLocal()

        try:
            policy = db.get(Policy, policy_id)

            if not policy or policy.car_id != car_id:
                return Response(error_response(404, "Policy not found for this car"), status=404)

            car = db.get(Car, policy.car_id)
            if not car:
                return Response(error_response(404, "Car not found"), status=404)

            db.delete(policy)
            db.commit()

            logger.info(
                "Policy deleted",
                policy_id=policy.id,
                car_id=policy.car_id,
                provider=policy.provider,
                start_date=str(policy.start_date),
                end_date=str(policy.end_date)
            )

            return Response(status=204)
        finally:
            db.close()


class InsuranceValidityView(APIView):

    def get(self, request, car_id):
        db = SessionLocal()

        try:
            date_str = request.GET.get("date")

            if not date_str:
                return Response(error_response(400, "Missing date query parameter"), status=400)

            try:
                target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return Response(error_response(400, "Invalid date format, expected YYYY-MM-DD with a valid date"), status=400)

            if not (1900 <= target_date.year <= 2100):
                return Response(error_response(400, "Date year must be between 1900 and 2100"), status=400)

            car = db.get(Car, car_id)
            if not car:
                return Response(error_response(404, "Car not found"), status=404)

            valid = valid_car_and_policy(db, car_id, target_date)
            response_data = {
                "carId": car_id,
                "date": date_str,
                "valid": valid
            }

            return Response(response_data, status=200)

        finally:
            db.close()
