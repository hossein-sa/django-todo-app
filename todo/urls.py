from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('add/', views.add_task, name='add_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('toggle/<int:task_id>/', views.toggle_task_status, name='toggle_task_status'),
    
    path('delete_all/', views.delete_all_tasks, name='delete_all_tasks'),
    path('delete_completed/', views.delete_completed_tasks, name='delete_completed_tasks'),
]
