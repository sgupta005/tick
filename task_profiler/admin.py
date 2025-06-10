from django.contrib import admin
from .models import Profile, TaskLog, CronJobStatus
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'slack_auth')
    search_fields = ('user__username', 'slack_auth')
    readonly_fields = ('user',)
    ordering = ('id',)

    # save the user who created the profile
    def save_model(self, request, obj, form, change):
        if not obj.pk: 
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(TaskLog)
class TaskLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'created_at', 'updated_at')
    search_fields = ('task__name',)
    ordering = ('id',)

@admin.register(CronJobStatus)
class CronJobStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_running', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('id',)


