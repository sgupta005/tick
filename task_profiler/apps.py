from django.apps import AppConfig


class TaskProfilerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task_profiler'

    # import the signals
    def ready(self):
        import task_profiler.signals
