from django.contrib import admin
from .models import Topic, Assignee, Task

# Register your models here.
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slack_channel_id', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'slack_channel_id')
    list_editable = ('is_active',)
    
@admin.register(Assignee)
class AssigneeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'slack_user_id')
    list_filter = ('is_active',)
    search_fields = ('name', 'slack_user_id')
    list_editable = ('is_active',)
    
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'assignee', 'due_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'assignee__name')
    list_editable = ('is_active',)


