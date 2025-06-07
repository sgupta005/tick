from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('oauth/callback/', views.slack_oauth_callback, name='slack_oauth_callback'),
]