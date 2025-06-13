import os
import django
import datetime

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tick.settings')
django.setup()

from django.contrib.auth.models import User
from planner.models import Workspace, Topic, Assignee, Task

def populate_database():
    """
    Populates the database with initial data for Workspaces, Topics, Assignees, and Tasks.
    """
    print("Starting database population...")

    # --- 1. GET OR CREATE A USER ---
    # We need a user to associate with Topics and Tasks.
    # The script will use the first superuser found, or create one if none exist.
    if User.objects.filter(is_superuser=True).exists():
        admin_user = User.objects.filter(is_superuser=True).first()
        print(f"Using existing superuser: {admin_user.username}")
    else:
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        print(f"Created new superuser: {admin_user.username} (password: password)")

    # --- 2. DEFINE YOUR DATA ---
    # Modify the values below to fit your needs.
    # Especially the placeholders like 'YOUR_BOT_TOKEN_HERE'.

    workspaces_data = [
        {
            'name': 'EFI',
            # --- ENTER YOUR BOT TOKEN HERE ---
            'bot_token': 'xoxb-9011218437620-9016283349026-9xFrWOMuu6ZYpsKCyYrFb1SG',
            'topics': [
                {
                    'name': 'Deal Scanner',
                    # --- ENTER YOUR SLACK CHANNEL HERE ---
                    'slack_channel': 'C090B6EPN3E',
                    'tasks': [
                        {'name': 'Design new logo', 'assignee_name': 'Advita'},
                        {'name': 'Develop landing page', 'assignee_name': 'Advita'},
                    ]
                },
                {
                    'name': 'Marketing Campaign',
                    # --- ENTER YOUR SLACK CHANNEL HERE ---
                    'slack_channel': 'C090B6EPN3E',
                    'tasks': [
                        {'name': 'Write blog post', 'assignee_name': 'Advita'},
                        {'name': 'Create social media assets', 'assignee_name': 'Advita'},
                    ]
                }
            ]
        }
    ]

    assignees_data = [
        {'name': 'Advita', 'slack_user': 'U08VAA05QEB'},
    ]

    # --- 3. CREATE ASSIGNEES ---
    print("\n--- Creating Assignees ---")
    assignee_objects = {}
    for assignee_info in assignees_data:
        assignee, created = Assignee.objects.get_or_create(
            name=assignee_info['name'],
            defaults={'slack_user': assignee_info['slack_user']}
        )
        assignee_objects[assignee.name] = assignee
        if created:
            print(f"  Created Assignee: {assignee.name}")
        else:
            print(f"  Assignee already exists: {assignee.name}")


    # --- 4. CREATE WORKSPACES, TOPICS, AND TASKS ---
    print("\n--- Creating Workspaces, Topics, and Tasks ---")
    for ws_data in workspaces_data:
        # Create Workspace
        workspace, created = Workspace.objects.get_or_create(
            name=ws_data['name'],
            defaults={'bot_token': ws_data['bot_token']}
        )
        if created:
            print(f"Created Workspace: {workspace.name}")
        else:
            print(f"Workspace already exists: {workspace.name}")

        # Create Topics for the Workspace
        for topic_data in ws_data.get('topics', []):
            topic, created = Topic.objects.get_or_create(
                workspace=workspace,
                name=topic_data['name'],
                defaults={
                    'user': admin_user,
                    'slack_channel': topic_data['slack_channel']
                }
            )
            if created:
                print(f"  Created Topic: {topic.name}")
            else:
                print(f"  Topic already exists: {topic.name}")
            
            # Create Tasks for the Topic
            for task_data in topic_data.get('tasks', []):
                assignee_name = task_data['assignee_name']
                assignee_obj = assignee_objects.get(assignee_name)

                if not assignee_obj:
                    print(f"    - WARNING: Assignee '{assignee_name}' not found. Skipping task '{task_data['name']}'.")
                    continue

                task, created = Task.objects.get_or_create(
                    topic=topic,
                    name=task_data['name'],
                    defaults={
                        'user': admin_user,
                        'assignee': assignee_obj,
                        'due_date': datetime.date.today()
                    }
                )
                if created:
                    print(f"    - Created Task: {task.name}")
                else:
                    print(f"    - Task already exists: {task.name}")

    print("\nDatabase population complete.")

if __name__ == '__main__':
    populate_database() 