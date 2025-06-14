# views.py
import requests
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.management import call_command
from .models import CronJobStatus, Question, Reply
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from planner.models import Topic
from django.db.models import Count
from .utils import convert_slack_timestamp

def landing_page(request):
    """Landing page that redirects based on authentication status"""
    if request.user.is_authenticated:
        return redirect('system_health')
    else:
        return redirect('login')

def slack_oauth_callback(request):
    code = request.GET.get("code")
    if not code:
        return HttpResponse("No code received")

    response = requests.post("https://slack.com/api/oauth.v2.access", data={
        "client_id": settings.SLACK_APP_CLIENT_ID,
        "client_secret": settings.SLACK_APP_CLIENT_SECRET,
        "code": code,
        "redirect_uri": settings.REDIRECT_URI
    })

    data = response.json()
    print(data)
    if data.get("ok"):
        access_token = data.get("authed_user").get("access_token")  # This is your new xoxp token
        return HttpResponse(f"Success! User token: {access_token}")
    else:
        return HttpResponse(f"OAuth failed: {data.get('error')}")

@never_cache
@login_required
def system_health(request):
    """Display the cronjob control dashboard"""
    status = CronJobStatus.get_status()
    return render(request, 'task_profiler/system_health.html', {
        'cron_enabled': status.is_running
    })


@never_cache
@login_required
def toggle_cronjob(request):
    """Toggle cronjobs on/off"""
    if request.method == 'POST':
        status = CronJobStatus.get_status()
        
        try:
            if status.is_running:
                # Stop cronjobs
                call_command('crontab', 'remove')
                status.is_running = False
                status.save()
                messages.success(request, 'Cronjobs stopped successfully!')
            else:
                # Start cronjobs
                call_command('crontab', 'add')
                status.is_running = True
                status.save()
                messages.success(request, 'Cronjobs started successfully!')
                
        except Exception as e:
            messages.error(request, f'Error toggling cronjobs: {str(e)}')
    
    return redirect('system_health')

@never_cache
@login_required
def report(request):
    # Get all active topics with their related data
    topics = Topic.objects.filter(is_active=True).annotate(
        num_questions=Count('task__question', distinct=True)
    ).prefetch_related(
        'task_set__question_set__reply_set'
    ).order_by('name')
    
    return render(request, 'task_profiler/report.html', {
        'topics': topics,
    })