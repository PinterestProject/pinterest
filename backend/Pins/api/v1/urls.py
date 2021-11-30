from django.urls import path

from Pins.api.v1.views import (
    PinDetails,
    PinList,
    get_board_pins
)

app_name = "Pins-v1"

urlpatterns = [
    path("api/v1/pins/", PinList.as_view(), name="pins"),
    path("api/v1/pins/<int:pk>/", PinDetails.as_view(), name="pin-details"),
    path("api/v1/boards/<int:pk>/pins/", get_board_pins, name="board-pin-details"),
]
