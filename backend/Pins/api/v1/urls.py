from django.urls import path
from rest_framework import views

from Pins.api.v1.views import PinDetails, PinList, get_board_pins, get_user_pins, pinsOfSpecificCategory,

app_name = "Pins-v1"

urlpatterns = [
    path("api/v1/pins/", PinList.as_view(), name="pins"),
    path("api/v1/pins/<int:pk>/", PinDetails.as_view(), name="pin-details"),
    path("api/v1/boards/<int:pk>/pins/", get_board_pins, name="board-pin-details"),
    path("api/v1/user/pins/", get_user_pins, name="get-user-pins"),
    path("api/v1/categories/pins/",pinsOfSpecificCategory),
]
