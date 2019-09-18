from django.db import models
from gmail_authentication.models import *

class Votes(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    votes = models.IntegerField()
    comment = models.TextField()
    datetime_voted = models.DateTimeField(auto_now_add=True)
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.datetime_voted)
