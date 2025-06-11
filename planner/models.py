from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Workspace(models.Model):
    name = models.CharField(max_length=200)
    bot_token = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Topic(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slack_channel = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
class Assignee(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    slack_user= models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    assignee = models.ForeignKey(Assignee, on_delete=models.CASCADE)
    due_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    

    

    
    
    