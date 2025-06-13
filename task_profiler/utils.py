from planner.models import Task
from .models import Question, Reply
from datetime import datetime

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


