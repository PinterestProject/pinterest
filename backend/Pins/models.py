from django.db import models
<<<<<<< HEAD
from Users.models import User
from Boards.models import Board
=======
# from Users.models import User
>>>>>>> origin/dev
from datetime import datetime
from Categories.models import Category
from Boards.models import Board
# Create your models here.


class Pin(models.Model):
    """
    Pins Table
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    attachment = models.ImageField(upload_to="uploads/pins/")
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    boards = models.ManyToManyField(Board)
    categories = models.ManyToManyField(Category)

    def __str__(self) -> str:
        return f"{self.title}"


class Favourite(models.Model):

    date = models.DateTimeField(default=datetime.now, blank=True)
    user_id = models.ForeignKey("Users.User", on_delete=models.CASCADE)
    pin_id = models.ForeignKey(Pin, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_id', 'pin_id',)

    def __str__(self):
        return f'{self.user_id.name} {self.pin_id.title}'

