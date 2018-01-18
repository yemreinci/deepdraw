from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):

    data = models.CharField(max_length=512*1024)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=10, default='-')