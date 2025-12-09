"""
URL Configuration for Bot App
"""
from django.urls import path
from . import views

app_name = 'bot'

urlpatterns = [
    # Main bot endpoint - Microsoft Bot Service sends messages here
    path('api/messages/', views.messages, name='messages'),
    
    # Health check endpoint
    path('health/', views.health_check, name='health'),
    
    # Bot information endpoint
    path('info/', views.bot_info, name='info'),
]