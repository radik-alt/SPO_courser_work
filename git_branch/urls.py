from django.contrib import admin
from django.urls import path

from git_branch.views import *

urlpatterns = [
    path('levels', LevelsApi.as_view()),
    path('tasks', TaskApi.as_view()),
    path('tasks/<int:level>/', TaskFromLevel.as_view()),
    path('task_info/<int:task_id>/', TaskInfoApiView.as_view()),
    path('git_info', GitInfoApiView.as_view()),
    path('grapth/<int:task_id>/', GetGraphOfTask.as_view())
]
