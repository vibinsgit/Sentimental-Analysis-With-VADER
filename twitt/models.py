from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Chat(models.Model):
    text = models.CharField(max_length=500)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    positive = models.FloatField(default=0.0)
    negative = models.FloatField(default=0.0)
    neutral = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return super().__str__(self.user)