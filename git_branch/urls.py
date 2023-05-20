from django.contrib import admin
from django.urls import path

from git_branch.views import *

urlpatterns = [
    path('api/v1/levels', LevelsApi.as_view()),
    path('api/v1/tasks', TaskApi.as_view()),
    path('api/v1/tasks/<int:level>/', TaskFromLevel.as_view()),
    path('api/v1/task_info/<int:task_id>/', TaskInfoApiView.as_view()),
    path('api/v1/git_info', GitInfoApiView.as_view())
]
