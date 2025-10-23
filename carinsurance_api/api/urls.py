from django.urls import path

from carinsurance_api.api.routers.cars import CarView
from carinsurance_api.api.routers.claims import ClaimView
from carinsurance_api.api.routers.history import HistoryView
from carinsurance_api.api.routers.policies import (InsuranceValidityView,
                                                   PolicyView)

urlpatterns = [
    path("", CarView.as_view()),
    path("<int:car_id>/", CarView.as_view()),
    path("<int:car_id>/policies/", PolicyView.as_view()),
    path("<int:car_id>/policies/<int:policy_id>/", PolicyView.as_view()),
    path("<int:car_id>/insurance-valid/", InsuranceValidityView.as_view()),
    path("<int:car_id>/claims/", ClaimView.as_view()),
    path("<int:car_id>/claims/<int:claim_id>/", ClaimView.as_view()),
    path("<int:car_id>/history/", HistoryView.as_view())
]
