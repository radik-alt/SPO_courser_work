from typing import List

from django.http import HttpResponse
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
                "description": "Просмотр истории коммитов с изменениями", "command": "git log -p"
            }
        ]

        return Response({
            "commands": commands,
            "status": status,
            "message": message
        })


class GetGraphOfTask(APIView):

    def get(self, request, task_id):
        nodes = Node.objects.filter(task_id=task_id)
        nodes_serializer = NodeSerializer(nodes, many=True)

        nodes_solve = NodeSolve.objects.filter(task_id=task_id)
        node_solve_serializer = NodeSolveSerializer(nodes_solve, many=True)

        return Response(
            {
                "started_graph": nodes_serializer.data,
                "solve_graph": node_solve_serializer.data,
                "remote_graph": None,
                "solve_remote_graph": None,
                "status": 0,
                "message": "Графы по задаче"
            }
        )


class Node:
    def __init__(self):
        self.name = ""
        self.parent = []
        self.children = []
        self.branch = []
        self.currentBranch = ""
        self.currentNode = False


class Model:
    def __init__(self):
        self.data = []
        self.command = ""


class WorkGraph(APIView):

    def post(self, request):
        data = request.data  # Get the request body

        # Parse the request body and create a Model object
        model = Model()
        model.data = self.parse_data(data.get("data", []))
        model.command = data.get("command", "")

        status = 0
        message = "Success"
        try:
            if self.valid(command=model.command):
                _commad = model.command.split()
                if _commad[0] != "git":
                    raise Exception("")

                if _commad[1] == "commit":
                    pass
                elif _commad[1] == "checkout":
                    message = self.get_name(model.command)
                    pass
                elif _commad[1] == "branch":
                    message = self.get_name(model.command)
                    pass
                elif _commad[1] == "push":
                    pass
                elif _commad[1] == "clone":
                    pass
            else:
                status = -1
                message = "Нет такой команды, проверьте правильно ли вы прописали команду"
        except:
            return Response({"data": None, "message": "Ошибка! Проверьте свою на правильно написана ли ваша команда", "code": -1})


        # Perform necessary operations with the received data
        # ...

        return Response({"data": None, "message": message, "code": status})

    def get_name(self, commands:str):
        return commands.split()[2]

    def all_commands(self) -> list:
        return ["commit", "push", "branch", "checkout", "pull", "clone", "fetch"]

    def valid(self, command) -> bool:
        split_list = command.split()
        first_word = split_list[0]
        second_word = split_list[1]
        return first_word == "git" and second_word in self.all_commands()

    def parse_data(self, data: List[dict]) -> List[Node]:
        nodes = []

        for item in data:
            node = Node()
            node.name = item.get("name", "")
            node.parent = self.parse_nodes(item.get("parent", []))
            node.children = self.parse_nodes(item.get("children", []))
            node.branch = item.get("branch", [])
            node.currentBranch = item.get("currentBranch", "")
            node.currentNode = item.get("currentNode", False)

            nodes.append(node)

        return nodes

    def parse_nodes(self, nodes: List[dict]) -> List[Node]:
        parsed_nodes = []

        for item in nodes:
            node = Node()
            node.name = item.get("name", "")
            node.parent = self.parse_nodes(item.get("parent", []))
            node.children = self.parse_nodes(item.get("children", []))
            node.branch = item.get("branch", [])
            node.currentBranch = item.get("currentBranch", "")
            node.currentNode = item.get("currentNode", False)

            parsed_nodes.append(node)

        return parsed_nodes
