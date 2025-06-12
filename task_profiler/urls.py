from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('slack/oauth/callback/', views.slack_oauth_callback, name='slack_oauth_callback'),
    path('system-health/', views.system_health, name='system_health'),
    path('toggle-cronjob/', views.toggle_cronjob, name='toggle_cronjob'),
    path('report/', views.report, name='report'),
]