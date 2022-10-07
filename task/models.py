from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    t_name = models.CharField(max_length=100)
    note = models.TextField(blank=True)
    priority = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    completiondate = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return self.t_name