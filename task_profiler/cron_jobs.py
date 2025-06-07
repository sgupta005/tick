from task_profiler.models import TaskLog
from task_profiler.utils import get_active_tasks_for_today

def create_tasklogs():
    print("Starting to process tasks for today...")
    
    try:
        active_tasks = get_active_tasks_for_today()

        if not active_tasks.exists():
            print("No active tasks for today.")
            return

        print(f"Found {len(active_tasks)} active task(s).")

        for task in active_tasks:
            TaskLog.objects.create(
                task=task,
            )
            print(f"Successfully created TaskLog for: '{task.name}'")
        
        print("Finished processing all tasks for today.")

    except Exception as e:
        print(f"An error occurred: {e}")