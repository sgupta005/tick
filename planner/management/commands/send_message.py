from django.core.management.base import BaseCommand
from planner.models import Task

class Command(BaseCommand):
    help = 'Prints the names of all tasks in the database'

    def handle(self, *args, **options):
        tasks = Task.objects.all()
        if tasks:
            self.stdout.write(self.style.SUCCESS('Found the following tasks:'))
            for task in tasks:
                self.stdout.write(f'- {task.name}')
        else:
            self.stdout.write(self.style.WARNING('No tasks found in the database.')) 