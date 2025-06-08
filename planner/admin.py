from django.contrib import admin
from .models import Topic, Assignee, Task, Workspace, Question
from .forms import QuestionInlineForm

# Register your models here.
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slack_channel', 'is_active', 'user')
    list_filter = ('is_active',)
    search_fields = ('name', 'slack_channel')
    list_editable = ('is_active',)
    readonly_fields = ('user',)
    ordering = ('id',)
    

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
    ordering = ('id',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'task', 'answer')
    list_filter = ('task',)
    search_fields = ('question', 'task__name')
    ordering = ('id',)

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    form = QuestionInlineForm
    
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'topic', 'assignee', 'due_date', 'is_active', 'user')
    list_filter = ('is_active', 'topic', 'assignee')
    search_fields = ('name', 'assignee__name', 'topic__name')
    list_editable = ('is_active',)
    readonly_fields = ('user',)
    ordering = ('id',)
    inlines = [QuestionInline]

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # When creating a new object
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    list_editable = ('is_active',)
    ordering = ('id',)

