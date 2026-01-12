from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    from_place = models.CharField(max_length=100)
    to_place = models.CharField(max_length=100)
    duration = models.IntegerField()
    budget = models.IntegerField()

    def __str__(self):
        return self.name
