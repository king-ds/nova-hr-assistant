from django.db import models
from gmail_authentication.models import *

# Create your models here.
class Votes(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    votes = models.IntegerField()
    datetime_voted = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        return str(self.datetime_vote)
