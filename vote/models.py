from django.db import models
from gmail_authentication.models import *

# Create your models here.
class Votes(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    votes = models.IntegerField()
    comment = models.TextField()
    datetime_voted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.datetime_voted)
