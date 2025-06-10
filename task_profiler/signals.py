from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TaskLog
from .opeanai import get_question_from_openai
from .slack import send_slack_message
from .utils import create_question_for_task

@receiver(post_save, sender=TaskLog)
def task_log_post_save(sender, instance, created, **kwargs):
    """
    This signal runs after a TaskLog instance is saved.
    """
    if created:
        # send message to chatgpt to frame a formal question
        openai_result = get_question_from_openai(instance.task)
        question = openai_result["output"]
        instance.openai_log = openai_result["openai_response"]
        # send the question to slack
        slack_result = send_slack_message(question,instance.task)
        question_ts = slack_result["ts"]
        instance.slack_post_log = slack_result["slack_response"]
        # use the question to create a new question object
        question_obj = create_question_for_task(instance.task, question, question_ts)
        instance.question = question_obj
        # save the changes made to tasklog
        instance.save()
        
