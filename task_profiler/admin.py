from django.contrib import admin
from .models import Profile, TaskLog, CronJobStatus, Question, Reply
from .forms import ReplyInlineForm
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'slack_auth', 'created_at', 'updated_at')
    search_fields = ('user__username', 'slack_auth')
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
    ordering = ('id',)

class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 0
    form = ReplyInlineForm

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question','is_pending', 'task', 'timestamp', 'created_at', 'updated_at')
    list_filter = ('task',)
    search_fields = ('question', 'task__name')
    ordering = ('id',)
    inlines = [ReplyInline]

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text', 'slack_user', 'timestamp', 'created_at', 'updated_at')
    list_filter = ('question',)
    search_fields = ('question__question', 'text', 'slack_user')
    ordering = ('id',)


