from django.contrib import admin
from django.urls import path

from git_branch.views import LevelsApi, TaskApi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/levels', LevelsApi.as_view()),
]
