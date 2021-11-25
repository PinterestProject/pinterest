from django.urls import path

from Boards.api.v1.views import (
    BoardList,
    BoardDetails,
)

app_name = "Boards-v1"

urlpatterns = [
    path("api/v1/boards/", BoardList.as_view(), name="boards"),
    path("api/v1/boards/<int:pk>/", BoardDetails.as_view(), name="board-details"),
]
