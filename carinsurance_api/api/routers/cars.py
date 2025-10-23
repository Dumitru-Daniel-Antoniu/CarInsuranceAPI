from datetime import datetime

from pydantic import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from carinsurance_api.api.errors import error_response
from carinsurance_api.api.schemas import CarSchema, OwnerSchema
from carinsurance_api.db.models.car import Car
from carinsurance_api.db.models.owner import Owner
from carinsurance_api.db.session import SessionLocal
from carinsurance_api.services.validity_service import valid_car_and_policy


class CarView(APIView):

    def get(self, request, car_id=None):
        db = SessionLocal()

        try:
            if car_id is not None:
                car = db.get(Car, car_id)

                if not car:
                    return Response(error_response(404, "Car not found"), status=404)

                owner = db.get(Owner, car.owner_id)
                car_data = CarSchema.model_validate(car).model_dump(by_alias=True)
                owner_data = OwnerSchema.model_validate(owner).model_dump(by_alias=True)
                car_data["owner"] = owner_data

                return Response(car_data, status=200)

            else:
                cars = db.query(Car).all()
                response_data = []

                for car in cars:
                    owner = db.get(Owner, car.owner_id)
                    car_data = CarSchema.model_validate(car).model_dump(by_alias=True)
                    owner_data = OwnerSchema.model_validate(owner).model_dump(by_alias=True)
                    car_data["owner"] = owner_data
                    response_data.append(car_data)

                return Response(response_data, status=200)

        finally:
            db.close()


    def post(self, request):
        db = SessionLocal()
        try:
            data = request.data

            try:
                car_data = CarSchema.model_validate(data)
            except ValidationError as ve:
                return Response(error_response(422, "Car validation error", ve.errors()), status=422)

            if db.query(Car).filter_by(vin=car_data.vin).first():
                return Response(error_response(409, "VIN must be unique"), status=409)

            if not db.query(Owner).filter_by(id=car_data.owner_id).first():
                return Response(error_response(404, "Owner does not exist"), status=404)

            car = Car(**car_data.model_dump())
            db.add(car)
            db.commit()
            db.refresh(car)

            response_data = CarSchema.model_validate(car).model_dump(by_alias=True)
            return Response(response_data, status=201)

        finally:
            db.close()


    def delete(self, request, car_id):
        db = SessionLocal()

        try:
            car = db.get(Car, car_id)

            if not car:
                return Response(error_response(404, "Car not found"), status=404)

            db.delete(car)
            db.commit()

            return Response(status=204)

        finally:
            db.close()
