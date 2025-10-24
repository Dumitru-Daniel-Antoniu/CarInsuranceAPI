from pydantic import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from carinsurance_api.api.errors import error_response
from carinsurance_api.api.schemas import ClaimSchema
from carinsurance_api.core.core_logger import logger
from carinsurance_api.db.models.car import Car
from carinsurance_api.db.models.claim import Claim
from carinsurance_api.db.session import SessionLocal
from carinsurance_api.services.claim_service import create_claim


class ClaimView(APIView):
    def get(self, request, car_id, claim_id=None):
        db = SessionLocal()

        try:
            if claim_id is not None:
                claim = db.get(Claim, claim_id)

                if not claim or claim.car_id != car_id:
                    return Response(error_response(404, "Claim not found for this car"), status=404)

                response_data = ClaimSchema.model_validate(claim).model_dump(by_alias=True)

                return Response(response_data, status=200)

            else:
                car = db.get(Car, car_id)

                if not car:
                    return Response(error_response(404, "Car not found"), status=404)

                claims = db.query(Claim).filter_by(car_id=car_id).all()
                response_data = [ClaimSchema.model_validate(claim).model_dump(by_alias=True) for claim in claims]

                return Response(response_data, status=200)

        finally:
            db.close()


    def post(self, request, car_id):
        db = SessionLocal()

        try:
            data = request.data
            data["car_id"] = car_id

            try:
                claim_data = ClaimSchema.model_validate(data)
            except ValidationError as ve:
                if ve.errors()[0]['type'] == 'value_error':
                    return Response(error_response(422, "Claim validation error", ve.errors()[0]['msg']), status=422)
                else:
                    return Response(error_response(422, "Claim validation error", ve.errors()), status=422)

            car = db.get(Car, data["car_id"])
            if not car:
                return Response(error_response(404, "Car not found"), status=404)

            claim, location = create_claim(db, claim_data)
            response_data = ClaimSchema.model_validate(claim).model_dump(by_alias=True)

            logger.info(
                "Claim created",
                claim_id=claim.id,
                car_id=claim.car_id,
                claim_amount=claim.amount,
                claim_description=claim.description,
                claim_date=str(claim.claim_date)
            )

            return Response(response_data, status=201, headers={"Location": location})

        finally:
            db.close()


    def delete(self, request, car_id, claim_id):
        db = SessionLocal()

        try:
            claim = db.get(Claim, claim_id)

            if not claim or claim.car_id != car_id:
                return Response(error_response(404, "Claim not found for this car"), status=404)

            car = db.get(Car, claim.car_id)
            if not car:
                return Response(error_response(404, "Car not found"), status=404)

            db.delete(claim)
            db.commit()

            logger.info(
                "Claim deleted",
                claim_id=claim.id,
                car_id=claim.car_id,
                claim_amount=claim.amount,
                claim_description=claim.description,
                claim_date=str(claim.claim_date)
            )

            return Response(status=204)

        finally:
            db.close()
