"""health_log URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

app_name = 'health_logs'

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('topic/<int:topic_id>/', views.topic, name='topic'),
    path('topics/<int:topic_id>/<int:wrkt_topic_id>/', views.topic, name='topic'),
    
    path('new_topic/', views.new_topic, name='new_topic'),
    # Page for adding a new entry
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # Page for editing an entry.
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    
    
    path('topics_logs/', views.topics_logs, name='topics_logs'),
    path('topics_logs/<int:topic_id>/', views.topic_logs, name='topic_logs'),
    
    path('new_topic_logs/', views.new_topic_logs, name='new_topic_logs'),
    # Page for adding a new entry
    path('new_entry_logs/<int:topic_id>/', views.new_entry_logs, name='new_entry_logs'),
    # Page for editing an entry.
    path('edit_entry_logs/<int:entry_id>/', views.edit_entry_logs, name='edit_entry_logs'),
    
    
    path('topics_goals/', views.topics_goals, name='topics_goals'),
    path('topics_goals/<int:topic_id>/', views.topic_goals, name='topic_goals'),
    
    path('new_topic_goals/', views.new_topic_goals, name='new_topic_goals'),
    # Page for adding a new entry
    path('new_entry_goals/<int:topic_id>/', views.new_entry_goals, name='new_entry_goals'),
    # Page for editing an entry.
    path('edit_entry_goals/<int:entry_id>/', views.edit_entry_goals, name='edit_entry_goals'),
    
    
    path('topics_workouts/', views.topics_workouts, name='topics_workouts'),
    path('topics_workouts/<int:topic_id>/', views.topic_workouts, name='topic_workouts'),
    path('exercises_workouts/<int:topic_id>/', views.exercises_workouts, name='exercises_workouts'),
    path('do_workout/<int:topic_id>/', views.do_workout, name='do_workout'),
    path('update_workout_info/<int:topic_id>/', views.update_workout_info, name='update_workout_info'),
    path('link_workouts/<int:topic_id>/', views.link_workouts, name='link_workouts'),
    
    path('new_topic_workouts/', views.new_topic_workouts, name='new_topic_workouts'),
    # Page for adding a new entry
    path('new_entry_workouts/<int:topic_id>/', views.new_entry_workouts, name='new_entry_workouts'),
    # Page for editing an entry.
    path('edit_entry_workouts/<int:entry_id>/', views.edit_entry_workouts, name='edit_entry_workouts'),
    path('topics/ai_advisor/', views.ai_advisor, name='ai_advisor'),
    
    # path('generate_section/<int:entry_id>/', views.generate_section, name='generate_section'),
    # path('download/', views.download_template, name='download_template'),
    # path('download1/', views.download_result, name='download_result'),
 
    ]
