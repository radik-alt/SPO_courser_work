import os

import git
from django.http import HttpResponse
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

    def post(self, request):
        return Response({"status": -1, "message": "post запрос не разрешен! Иди нахуй Сагид!"})

    def update(self, requet):
        return Response({"status": -1, "message": "update запрос не разрешен"})

    def delete(self, request):
        return Response({"status": -1, "message": "update запрос не разрешен"})


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
            message = f"Список задач по id_ta"
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
                "message": "Error"
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

    def patch(self, request, task_id):
        task = Task.objects.filter(id=task_id)

        try:
            task.update(solve = request.data.get("solve"))
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
        message = "Список уровней"
        status = 0

        repo = git.Repo('.')
        commands = {}

        git_cmd = repo.git
        git_commands = git_cmd.execute(['help', '-a'], encoding='UTF-8', errors='ignore').splitlines()

        for command in git_commands:
            if not command.startswith(' '):
                command_name = command.split()[0]
                command_desc = ' '.join(command.split()[1:])
                commands[command_name] = command_desc
        return Response({
            "commands": commands,
            "status": status,
            "message": message
        })
