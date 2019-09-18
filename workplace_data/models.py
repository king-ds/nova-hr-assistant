from django.db import models

class Post(models.Model):
    group_id = models.CharField(max_length=255)
    post_id = models.CharField(max_length=255)
    message = models.TextField()
    updated_time = models.DateTimeField()
    
    def __str__(self):
        return self.post_id