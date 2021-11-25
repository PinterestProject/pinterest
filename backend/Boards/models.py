from django.db import models
# from Pins.models import Pin
# from Users.models import User


class Board(models.Model):
    """
    Boards Table
    each board must have a name
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    cover = models.ImageField(upload_to="uploads/boards/cover/")
    created_by = models.ForeignKey("Users.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)
    # pins = models.ManyToManyField(Pin)

    def __str__(self) -> str:
        return f"{self.name}"
