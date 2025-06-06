from planner.models import Task
from datetime import datetime

import logging
logging.basicConfig(level=logging.DEBUG)

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from dotenv import load_dotenv
load_dotenv()

def get_tasks_for_today():
    today = datetime.now().date()
    tasks = Task.objects.filter(due_date=today)
    return tasks

def send_slack_message(message):
    slack_token = os.getenv("SLACK_BOT_TOKEN")
    client = WebClient(slack_token)

    try:
        response = client.chat_postMessage(
            channel=os.getenv("SLACK_CHANNEL"),
            text=message
        )
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["error"]    # str like 'invalid_auth', 'channel_not_found'
