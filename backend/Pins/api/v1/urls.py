from django.urls import path

from Pins.api.v1.views import get_pins, create_pin

app_name = "Pins-v1"

urlpatterns = [
    path("api/v1/pins/", get_pins, name="pins"),
    # path("api/v1/pins/<int:pk>", pin_details, name="pin-details"),
    path("api/v1/pins/create", create_pin, name="create-pin"),
    # path("api/v1/pins/<int:pk>/edit", edit_pin, name="edit-pin"),
    # path("api/v1/pins/<int:pk>/delete", delete_pin, name="delete-pin"),
]
