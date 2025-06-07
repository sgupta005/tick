from planner.models import Task
from datetime import datetime

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from django.conf import settings

def get_active_tasks_for_today():
    today = datetime.now().date()
    tasks = Task.objects.filter(due_date=today, is_active=True)
    return tasks

def send_slack_message(message,channel,assignee):
    slack_token = settings.SLACK_BOT_TOKEN
    client = WebClient(slack_token)

    try:
        response = client.chat_postMessage(
            channel=channel,
            text=message
        )
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["error"]    # str like 'invalid_auth', 'channel_not_found'

# def send_slack_message_as_user(message):
#     slack_token = settings.SLACK_BOT_TOKEN
#     client = WebClient(slack_token)

#     try:
#         response = client.chat_postMessage(
#             channel=settings.SLACK_CHANNEL,
#             text=message
#         )
#     except SlackApiError as e:
#         # You will get a SlackApiError if "ok" is False
#         assert e.response["error"]    # str like 'invalid_auth', 'channel_not_found'
