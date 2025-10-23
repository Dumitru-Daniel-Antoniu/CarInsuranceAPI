from carinsurance_api.api.errors import error_response
from carinsurance_api.db.models.car import Car
from carinsurance_api.db.session import SessionLocal
from carinsurance_api.services.history_service import get_car_history

from rest_framework.response import Response
from rest_framework.views import APIView


class HistoryView(APIView):

    def get(self, request, car_id):
        db = SessionLocal()

        try:
            car = db.get(Car, car_id)

            if not car:
                return Response(error_response(404, "Car not found"), status=404)

            response_data = get_car_history(db, car_id)

            return Response(response_data, status=200)

        finally:
            db.close()
