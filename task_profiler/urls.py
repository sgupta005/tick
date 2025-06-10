from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('slack/oauth/callback/', views.slack_oauth_callback, name='slack_oauth_callback'),
    path('cron-dashboard/', views.cron_dashboard, name='cron_dashboard'),
    path('toggle-cronjob/', views.toggle_cronjob, name='toggle_cronjob'),
]