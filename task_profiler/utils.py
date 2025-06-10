from planner.models import Task, Question
from datetime import datetime
from django.conf import settings

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from openai import OpenAI
from task_profiler.prompt import QUESTION_PROMPT

def get_active_tasks_for_today():
    today = datetime.now().date()
    tasks = Task.objects.filter(due_date=today, is_active=True)
    return tasks

def get_question_from_openai(task):
    message = f"{task.name} - {task.topic.name}"
    client = OpenAI(
    api_key=settings.OPENAI_API_KEY
    )

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {"role": "system", "content": QUESTION_PROMPT},
        {"role": "user", "content": message}
    ]
    )

    output = completion.choices[0].message.content
    return {"output":output, "openai_response":completion}

def create_question_for_task(task, question, question_ts):
    question_obj = Question.objects.create(
        question=question,
        task=task,
        timestamp=question_ts
    )
    return question_obj

def send_slack_message(message,task):
    channel = task.topic.slack_channel
    assignee_slack_user = task.assignee.slack_user
    slack_bot_token = task.topic.workspace.bot_token

    client = WebClient(slack_bot_token)
    message_with_slack_user = f"<@{assignee_slack_user}> {message}"

    try:
        response = client.chat_postMessage(
            channel=channel,
            text=message_with_slack_user
        )
        return {"slack_response":response, "ts":response["ts"]}
    except SlackApiError as e:
        assert e.response["error"]   
        return {"slack_response":None, "ts":None}

def get_question_replies_from_slack(channel, question_ts):
    slack_token = settings.SLACK_BOT_TOKEN
    client = WebClient(token=slack_token)
    try:
        response = client.conversations_replies(
            channel=channel,
            ts=question_ts
        )
        print(response.get("messages"))
        return response.get("messages")  # First message is usually the parent
    except SlackApiError as e:
        print(f"Error fetching replies: {e.response['error']}")
        return []
