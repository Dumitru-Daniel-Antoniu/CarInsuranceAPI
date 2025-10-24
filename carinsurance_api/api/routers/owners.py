from pydantic import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from sqlalchemy.exc import IntegrityError

from carinsurance_api.api.errors import error_response
from carinsurance_api.api.schemas import OwnerSchema
from carinsurance_api.db.models.owner import Owner
from carinsurance_api.db.session import SessionLocal


class OwnerView(APIView):

    def get(self, request, owner_id=None):
        db = SessionLocal()

        try:
            if owner_id is not None:
                owner = db.get(Owner, owner_id)

                if not owner:
                    return Response(error_response(404, "Owner not found"), status=404)

                response_data = OwnerSchema.model_validate(owner).model_dump(by_alias=True)

                return Response(response_data, status=200)

            else:
                owners = db.query(Owner).all()
                response_data = [OwnerSchema.model_validate(owner).model_dump(by_alias=True) for owner in owners]

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

            owner = Owner(**owner_data.model_dump(exclude={"id"}))
            db.add(owner)
            try:
                db.commit()
            except IntegrityError as ie:
                db.rollback()
                return Response(error_response(422, "Owner email must be unique", str(ie)), status=422)

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
