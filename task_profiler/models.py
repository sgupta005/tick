from django.db import models
from django.contrib.auth.models import User
from planner.models import Task
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    slack_auth = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username


class TaskLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task.name
    
    