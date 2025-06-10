from django.core.management.base import BaseCommand
from django.conf import settings
from task_profiler.models import CronJob

class Command(BaseCommand):
    help = 'Syncs cron jobs from settings.py to the database'

    def handle(self, *args, **options):
        self.stdout.write('Syncing cron jobs...')
        cron_jobs = getattr(settings, 'CRONJOBS', [])

        for job in cron_jobs:
            job_path = job[1]
            cron_job, created = CronJob.objects.get_or_create(name=job_path)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created cron job: {job_path}'))
            else:
                self.stdout.write(f'Cron job already exists: {job_path}')

        self.stdout.write(self.style.SUCCESS('Finished syncing cron jobs.')) 