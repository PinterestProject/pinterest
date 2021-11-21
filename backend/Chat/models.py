from django.db import models
from Users.models import User
from datetime import datetime
# Create your models here.

class Chat(models.Model):

    message = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    sender_id = models.ForeignKey(User, related_name='sender',  on_delete=models.CASCADE)
    receiver_id = models.ForeignKey(User, related_name='receiver',  on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.sender_id.name} {self.receiver_id.name}'
