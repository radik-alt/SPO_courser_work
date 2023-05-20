from django.forms import model_to_dict
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from git_branch import models


def index(request):
    return HttpResponse("Главная страница")

class LevelsApi(APIView):
    def get(self, request):
        levels = models.Levels.objects.all().values()
        message = "Список уровней"
        status = 0
        if levels.count() == 0:
            levels = levels
            message = "Нет данных о уровнях"
            status = -1
        return Response({
            "levels": list(levels),
            "status" : status,
            "message": message
        })

    def post(self, request):
        return Response({"status": -1, "message": "post запрос не разрешен"})

    def update(self, requet):
        return Response({"status": -1, "message": "update запрос не разрешен"})

    def delete(self, request):
        return Response({"status": -1, "message": "update запрос не разрешен"})


class TaskApi(APIView):

    def get(self, request):
        return Response({""})


class TaskFromLevel(APIView):

    def get(self, request):
        return Response({""})