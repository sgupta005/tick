from django.contrib import admin
from .models import Topic, Assignee, Task, Workspace, Question, Reply
from .forms import QuestionInlineForm, ReplyInlineForm

# Register your models here.
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slack_channel', 'is_active', 'user')
    list_filter = ('is_active',)
    search_fields = ('name', 'slack_channel')
    list_editable = ('is_active',)
    readonly_fields = ('user',)
    ordering = ('id',)
    
    # save the user who created the topic
    def save_model(self, request, obj, form, change):
        if not obj.pk: 
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(Assignee)
class AssigneeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'slack_user')
    list_filter = ('is_active',)
    search_fields = ('name', 'slack_user')
    list_editable = ('is_active',)
    ordering = ('id',)

class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 0
    form = ReplyInlineForm

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question','is_pending', 'task', 'timestamp')
    list_filter = ('task',)
    search_fields = ('question', 'task__name')
    ordering = ('id',)
    inlines = [ReplyInline]

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

    # save the user who created the task
    def save_model(self, request, obj, form, change):
        if not obj.pk: 
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    list_editable = ('is_active',)
    ordering = ('id',)

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text', 'timestamp')
    list_filter = ('question',)
    search_fields = ('question__question', 'text')
    ordering = ('id',)
    readonly_fields = ('question',)
