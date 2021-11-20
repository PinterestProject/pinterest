from django.db import models
from Users.models import User
from Boards.models import Board
from Categories.models import Category


class Pin(models.Model):
    """
    Pins Table
    """

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    attachment = models.ImageField(upload_to="/uploads/pins/")
    users = models.ManyToManyField(User)
    boards = models.ManyToManyField(Board)
    categories = models.ManyToManyField(Category)

    def __str__(self) -> str:
        return f"{self.title}"
