from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TaskLog
from .utils import send_slack_message, get_question_from_openai, create_question_for_task, get_question_replies_from_slack

@receiver(post_save, sender=TaskLog)
def task_log_post_save(sender, instance, created, **kwargs):
    """
    This signal runs after a TaskLog instance is saved.
    """
    if created:
        # send message to chatgpt to frame a formal question
        question = get_question_from_openai(instance.task)
        # send the question to slack
        channel = instance.task.topic.slack_channel
        assignee_slack_user = instance.task.assignee.slack_user
        question_ts = send_slack_message(question,channel,assignee_slack_user)
        # use the question to create a new question object
        create_question_for_task(instance.task, question, question_ts)
        
