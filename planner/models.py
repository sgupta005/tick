from django.db import models

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)
    slack_channel_id = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
class Assignee(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    slack_user_id = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Task(models.Model):
    name = models.CharField(max_length=200)
    assignee = models.ForeignKey(Assignee, on_delete=models.CASCADE)
    due_date = models.DateField()
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    
    