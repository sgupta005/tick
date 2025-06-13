from planner.models import Task
from .models import Question, Reply
from datetime import datetime
import pytz

def get_active_tasks_for_today():
    today = datetime.now().date()
    tasks = Task.objects.filter(due_date=today, is_active=True)
    return tasks

def get_pending_questions_for_today():
    today = datetime.now().date()
    questions = Question.objects.filter(is_pending=True, task__due_date=today)
    return questions

def get_all_questions_for_today():
    today = datetime.now().date()
    questions = Question.objects.filter(task__due_date=today)
    return questions

def convert_slack_timestamp(slack_timestamp):
    try:
        # Convert string to float to handle seconds.microseconds
        timestamp_float = float(slack_timestamp)
        
        # Create datetime object from timestamp (UTC)
        dt_utc = datetime.fromtimestamp(timestamp_float, tz=pytz.UTC)
        
        # Convert to Gulf Standard Time (UTC+4)
        gulf_tz = pytz.timezone('Asia/Dubai')  # Dubai timezone is GST (UTC+4)
        dt_gst = dt_utc.astimezone(gulf_tz)
        
        # Format as requested: 'June 13, 2025 at 06:36 PM GST'
        return dt_gst.strftime('%B %d, %Y at %I:%M %p GST')
    except (ValueError, TypeError):
        # Return original timestamp if conversion fails
        return slack_timestamp

def create_question_for_task(task, question, question_ts):
    question_obj = Question.objects.create(
        question=question,
        task=task,
        timestamp=question_ts
    )
    return question_obj
    
def create_replies_for_question(question, replies):
    for reply in replies:
        if (not Reply.objects.filter(timestamp=reply.get("ts")).exists()):
            Reply.objects.create(
                question=question,
                text=reply.get("text"),
                replier_slack_user=reply.get("replier_slack_user"),
                replier_name = reply.get("replier_name"),
                timestamp=reply.get("ts")
            )


