from task_profiler.models import TaskLog
from task_profiler.utils import get_active_tasks_for_today, get_pending_questions_for_today, create_replies_for_question, get_all_questions_for_today
from task_profiler.slack import get_question_replies_from_slack

def create_tasklogs():
    print("Starting to process tasks for today...")
    
    try:
        active_tasks = get_active_tasks_for_today()

        if not active_tasks.exists():
            print("No active tasks for today.")
            return

        print(f"Found {len(active_tasks)} active task(s).")

        for task in active_tasks:
            if (not TaskLog.objects.filter(task=task).exists()):
                TaskLog.objects.create(
                    task=task,
                )
            print(f"Successfully created TaskLog for: '{task.name}'")
        
        print("Finished processing all tasks for today.")

    except Exception as e:
        print(f"An error occurred: {e}")

def check_pending_questions_replies():
    try:
        pending_questions = get_pending_questions_for_today()
        if not pending_questions.exists():
            print("No pending questions for today.")
            return
        print(f"Found {len(pending_questions)} pending question(s).")

        for question in pending_questions:
            result = get_question_replies_from_slack(question.task.topic.slack_channel, question.timestamp, question.task.topic.workspace.bot_token)
            question.thread = result.get("thread")
            replies = result.get("replies")
            if (len(replies) > 0):
                create_replies_for_question(question, replies)
                question.is_pending = False
            question.save()
        
        print("Finished processing all questions.")

    except Exception as e:
        print(f"An error occurred: {e}")


def check_all_quesitons_replies():
    try:
        questions = get_all_questions_for_today()
        if not questions.exists():
            print("No questions for today.")
            return
        print(f"Found {len(questions)} question(s).")

        for question in questions:
            result = get_question_replies_from_slack(question.task.topic.slack_channel, question.timestamp, question.task.topic.workspace.bot_token)
            question.thread = result.get("thread")
            replies = result.get("replies")
            if (len(replies) > 0):
                create_replies_for_question(question, replies)
                question.is_pending = False
            question.save()
        
        print("Finished processing all questions.")

    except Exception as e:
        print(f"An error occurred: {e}")