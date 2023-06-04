from django.contrib import admin
from django.urls import path, include

from git_branch.views import *

from swager import urlpatterns as swagger_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path("api/v1/", include('git_branch.urls'))
]

urlpatterns += swagger_url

