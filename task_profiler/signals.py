from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TaskLog
from .utils import send_slack_message

@receiver(post_save, sender=TaskLog)
def task_log_post_save(sender, instance, created, **kwargs):
    """
    This signal runs after a TaskLog instance is saved.
    """
    if created:
        task = instance.task.assignee.name + " - " + instance.task.name
        channel = instance.task.topic.slack_channel
        assignee = instance.task.assignee.name
        send_slack_message(task,channel,assignee)

        print(f"Task: {task}, Channel: {channel}, Assignee: {assignee}")
