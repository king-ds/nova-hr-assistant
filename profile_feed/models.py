from django.db import models
from gmail_authentication.models import User

class Reaction(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_given = models.IntegerField(default=0)
    reaction_received = models.IntegerField(default=0)
    reaction_type = models.CharField(max_length=100)

    def __str__(self):
        return '%s,%s'%(self.username, self.reaction_type)