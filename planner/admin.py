from django.contrib import admin
from .models import Topic, Assignee, Task, Profile

# Register your models here.
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slack_channel', 'is_active', 'user')
    list_filter = ('is_active',)
    search_fields = ('name', 'slack_channel')
    list_editable = ('is_active',)
    readonly_fields = ('user',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # When creating a new object
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(Assignee)
class AssigneeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'slack_user')
    list_filter = ('is_active',)
    search_fields = ('name', 'slack_user')
    list_editable = ('is_active',)
    
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'topic', 'assignee', 'due_date', 'is_active', 'user')
    list_filter = ('is_active', 'topic', 'assignee')
    search_fields = ('name', 'assignee__name', 'topic__name')
    list_editable = ('is_active',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # When creating a new object
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'slack_auth')
    search_fields = ('user__username', 'slack_auth')

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # When creating a new object
            obj.user = request.user
        super().save_model(request, obj, form, change)


