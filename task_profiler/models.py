from django.db import models
from django.contrib.auth.models import User
from planner.models import Task, Question
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    slack_auth = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username

class TaskLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    openai_log = models.TextField(blank=True, null=True)
    slack_post_log = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task.name

class CronJobStatus(models.Model):
    is_running = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cron Job Status"
        verbose_name_plural = "Cron Job Status"

    def __str__(self):
        return f"Cronjobs {'Running' if self.is_running else 'Stopped'}"

    @classmethod
    def get_status(cls):
        status, created = cls.objects.get_or_create(id=1, defaults={'is_running': False})
        return status
    
    