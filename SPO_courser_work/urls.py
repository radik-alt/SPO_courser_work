from django.contrib import admin
from django.urls import path

from git_branch.views import LevelsApi, index, TaskApi

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index),
    path('api/v1/levels', LevelsApi.as_view()),
    path('api/v1/tasks', TaskApi.as_view())
]
