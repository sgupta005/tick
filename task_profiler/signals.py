from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TaskLog
from .utils import send_slack_message

@receiver(post_save, sender=TaskLog)
def task_log_post_save(sender, instance, created, **kwargs):
    """
    This signal runs after a TaskLog instance is s [aved.
    """
    if created:
        message = f"<@{instance.task.assignee.slack_user}> {instance.task.name} - {instance.task.topic.name}"
        channel = instance.task.topic.slack_channel
        assignee = instance.task.assignee.name
        send_slack_message(message,channel,assignee)

        print(f"Message: {message}, Channel: {channel}, Assignee: {assignee}")
