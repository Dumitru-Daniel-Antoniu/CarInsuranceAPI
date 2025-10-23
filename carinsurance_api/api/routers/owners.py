from carinsurance_api.api.errors import error_response
from carinsurance_api.api.schemas import OwnerSchema
from carinsurance_api.db.models.owner import Owner
from carinsurance_api.db.session import SessionLocal

from pydantic import ValidationError

from rest_framework.response import Response
from rest_framework.views import APIView


class OwnerView(APIView):

    def get(self, request, owner_id):
        db = SessionLocal()

        try:
            owner = db.get(Owner, owner_id)

            if not owner:
                return Response(error_response(404, "Owner not found"), status=404)

            response_data = OwnerSchema.model_validate(owner).model_dump(by_alias=True)

            return Response(response_data, status=200)

        finally:
            db.close()


    def post(self, request):
        db = SessionLocal()

        try:
            data = request.data

            try:
                owner_data = OwnerSchema.model_validate(data)
            except ValidationError as ve:
                return Response(error_response(422, "Owner validation error", ve.errors()), status=422)

            owner = Owner(**owner_data.model_dump())
            db.add(owner)
            db.commit()
            db.refresh(owner)
            response_data = OwnerSchema.model_validate(owner).model_dump(by_alias=True)

            return Response(response_data, status=201)

        finally:
            db.close()


    def delete(self, request, owner_id):
        db = SessionLocal()

        try:
            owner = db.get(Owner, owner_id)

            if not owner:
                return Response(error_response(404, "Owner not found"), status=404)

            db.delete(owner)
            db.commit()

            return Response(status=204)

        finally:
            db.close()
