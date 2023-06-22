from django.contrib import admin
from django.urls import path, include

from git_branch.views import *

from swager import urlpatterns as swagger_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('api/v1/levels', LevelsApi.as_view(), name="levels"),
    path('api/v1/tasks', TaskApi.as_view(), name="tasks"),
    path('api/v1/tasks/<int:level>/', TaskFromLevel.as_view()),
    path('api/v1/task_info/<int:task_id>/', TaskInfoApiView.as_view()),
    path('api/v1/git_info', GitInfoApiView.as_view()),
    path('api/v1/grapth/<int:task_id>/', GetGraphOfTask.as_view()),
    path('api/v1/graph_work', WorkGraph.as_view()),
    path('api/v1/solve_graph', SolveGraphApi.as_view())
]

urlpatterns += swagger_url

