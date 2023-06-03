from django.http import HttpResponse, JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from git_branch import models
from git_branch.serializer import *


def index(request):
    return HttpResponse("Главная страница")


class LevelsApi(APIView):
    def get(self, request):
        levels = models.Levels.objects.all().values()

        if levels.count() == 0:
            levels = levels
            message = "Нет данных о уровнях"
            status = -1
        else:
            message = "Список уровней"
            status = 0

        return Response({
            "levels": LevelsSerializers(levels, many=True).data,
            "status": status,
            "message": message
        })


class TaskApi(APIView):
    def get(self, request):
        tasks = models.Task.objects.all().values()
        if tasks.count() == 0:
            message = "Нет данных о уровнях"
            status = -1
        else:
            message = f"Список всех задач"
            status = 0

        serializer = TaskSerializer(models.Task.objects.all(), many=True)
        return Response({
            "tasks": serializer.data,
            "status": status,
            "message": message
        })


class TaskFromLevel(APIView):

    def get(self, request, level):

        tasks = Task.objects.filter(level=level)
        if tasks.count() == 0:
            message = f"Нет данных о задаче по данном уровню"
            status = -1
        else:
            message = f"Список задач по уровню"
            status = 0

        serializer = TaskSerializer(tasks, many=True)

        return Response({
            "tasks": serializer.data,
            "status": status,
            "message": message
        })


class TaskInfoApiView(APIView):
    def get(self, request, task_id):
        try:
            tasks = Task.objects.filter(id=task_id)
        except:
            return Response({
                "tasks": [],
                "status": -1,
                "message": "Error базы данных"
            })

        if tasks.count() == 0:
            message = f"Нет данных о задаче по данном task_id"
            status = -1
        else:
            message = f"Список задач по task_id"
            status = 0

        serializer = TaskSerializer(tasks, many=True)

        return Response({
            "tasks": serializer.data,
            "status": status,
            "message": message
        })

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'solve': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            }
        )
    )
    def patch(self, request, task_id):
        task = Task.objects.filter(id=task_id)

        try:
            task.update(solve=request.data.get("solve"))
        except:
            response = Response({
                "status": -1,
                "message": "Ошибка обнолвения данных"
            })
            response.status_code = 400
            return response

        message = "Данные обновлены"
        status = 0

        return Response({
            "status": status,
            "message": message
        })


class GitInfoApiView(APIView):

    def get(self, request):
        message = "Список команды для git"
        status = 0

        commands = [
            {
                "description": "Как задать имя пользователя и адрес электронной почты",
                "command": f"git config --global user.name 'username' \n git config --global user.email 'email' "
            },
            {
                "description": "Инициализация репозитория",
                "command": "git init",
            },
            {
                "description": "Добавление отдельных файлов или всех файлов в область подготовленных файлов",
                "command": "git add file.расширение либо git add . (для всех файлов)",
            },
            {
                "description": "Проверка статуса репозитория", "command": "git status",
            },
            {
                "description": "Внесение изменений однострочным сообщением или через редактор",
                "command": "git commit -m 'commit' либо git commit"
            },
            {
                "description":"Просмотр истории коммитов с изменениями", "command": "git log -p"
            }
        ]

        return Response({
            "commands": commands,
            "status": status,
            "message": message
        })

