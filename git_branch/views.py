from typing import List

from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.utils import json
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
        self.id = 1
        self.name = ""
        self.parent = []
        self.children = []
        self.branch = []
        self.currentBranch = ""
        self.currentNode = False
        self.type = 0

    def __str__(self):
        return f"Node(name={self.name}, parent={self.parent}, children={self.children}, " \
               f"branch={self.branch}, currentBranch={self.currentBranch}, currentNode={self.currentNode})"

    def to_dict(self):
        return {
            "name": self.name,
            "parent": [node.to_dict() for node in self.parent],
            "children": [node.to_dict() for node in self.children],
            "branch": self.branch,
            "currentBranch": self.currentBranch,
            "currentNode": self.currentNode
        }

    @classmethod
    def from_dict(cls, data):
        node = cls()
        node.name = data.get("name", "")
        node.parent = [cls.from_dict(item) for item in data.get("parent", [])]
        node.children = [cls.from_dict(item) for item in data.get("children", [])]
        node.branch = data.get("branch", [])
        node.currentBranch = data.get("currentBranch", "")
        node.currentNode = data.get("currentNode", False)
        return node


class Model:
    def __init__(self):
        self.data = []
        self.command = ""


class WorkGraph(APIView):

    def post(self, request):

        try:
            data = request.data  # Get the request body

            # Parse the request body and create a Model object
            model = Model()
            model.data: List[Node] = self.parse_data(data.get("data", []))
            model.command = data.get("command", "")
            model.task_id = data.get("task_id")

            status = 0
            message = "Success"

            if self.valid(command=model.command):
                _commad = model.command.split()
                if _commad[0] != "git":
                    raise Exception("")
                print(_commad)
                if _commad[1] == "commit":
                    if self.find_node_by_checkout(model.data, True, None) is None:
                        raise Exception()
                    else:
                        self.commit(model.data)

                elif _commad[1] == "checkout":
                    name = self.get_name(model.command)
                    if self.find_node_by_checkout(model.data, True, name) is None:
                        raise Exception()
                    else:
                        self.update_current_node(model.data, name)

                elif _commad[1] == "branch":
                    name = self.get_name(model.command)
                    self.add_branch(model.data, name)

                elif _commad[1] == "merge":
                    name = self.get_name(model.command)
                    self.merge(model.data, name)

                elif _commad[1] == "push":
                    pass
                elif _commad[1] == "clone":
                    pass

            else:
                raise Exception()
        except:
            response = Response(
                {
                    "data": None,
                    "remote_data": None,
                    "message": "Ошибка! Проверьте правильно написана ли ваша команда",
                    "code": -1
                })
            response.status_code = 200
            return response

            # Perform necessary operations with the received data
        # ...
        serialized_nodes = json.dumps([node.to_dict() for node in model.data])

        return Response({
            "data": serialized_nodes,
            "remote_data": None,
            "message": message,
            "code": status})

    def get_name_checkout_node(self, name):
        return f"*{name}"

    def merge(self, nodes: List[Node], name: str):
        node = self.find_node_by_checkout(nodes, True, None)
        if not name == node.currentBranch:
            origin = self.find_last_node_by_branch(nodes[0], name)
            merge = self.merge_nodes(node, origin)
            node.children.append(merge)
            origin.children.append(merge)

            origin.branch.remove(origin.currentBranch)
            origin.currentBranch = ""
        else:
            raise Exception()

    def commit(self, nodes: List[Node]):
        node = self.find_node_by_checkout(nodes, True, None)
        new_commit = self.create_node(name="C", parent=[], children=[], branch=[node.currentBranch],
                                      current_branch=node.currentBranch, current_node=True)
        node.branch.remove(self.get_name_checkout_node(node.currentBranch))
        node.currentBranch = ""
        node.currentNode = False

        node.children.append(new_commit)

    def find_last_node_by_branch(self, node: Node, target_current_branch: str) -> Node or None:
        if node.currentBranch == target_current_branch:
            return node

        last_node = None
        for child in node.children:
            child_node = self.find_last_node_by_branch(child, target_current_branch)
            if child_node:
                last_node = child_node

        return last_node

    def merge_nodes(self, node1: Node, node2: Node) -> Node:
        merged_node = Node()
        merged_node.name = "C"
        merged_node.children = []
        merged_node.parent = []
        merged_node.currentBranch = node2.currentBranch
        merged_node.currentNode = node1.currentNode
        merged_node.type = 2
        return merged_node

    def create_node(self, name: str, parent: [], children: [], branch: List[str] or None, current_branch: str,
                    current_node: bool):
        node = Node()
        node.name = name
        node.parent = parent or []
        node.children = children or []
        node.branch = branch or []
        node.currentBranch = current_branch
        node.currentNode = current_node

        return node

    def get_name(self, commands: str):
        return commands.split()[2]

    def all_commands(self) -> list:
        return ["commit", "push", "branch", "checkout", "pull", "clone", "fetch", "merge"]

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

    def add_branch(self, nodes: List[Node], target_current_branch: str):
        for node in nodes:
            if node.currentNode:
                node.branch.append(target_current_branch)
            self.add_branch(node.children, target_current_branch)
            # self.update_current_node(node.children, target_current_branch)

    def update_current_node(self, nodes: List[Node], target_current_branch: str):
        for node in nodes:
            node.currentNode = False  # Установка значения currentNode в False для всех узлов
            node.branch = [branch.replace(self.get_name_checkout_node(node.currentBranch), node.currentBranch) for
                           branch in
                           node.branch]
            print(target_current_branch)

            if node.currentBranch == target_current_branch:
                if not node.children:
                    node.currentBranch = target_current_branch
                    node.currentNode = True
                    node.branch = [branch.replace(target_current_branch, f"*{target_current_branch}") for branch in
                                   node.branch]
            else:
                node.currentBranch = ""

            self.update_current_node(node.children, target_current_branch)

    def update_current_node_start(self, nodes: List[Node], target_current_branch: str):
        for node in nodes:
            if len(node.branch) >= 2:
                if not node.children:
                    node.currentBranch = target_current_branch
                    node.currentNode = True
                    node.branch = [branch.replace(target_current_branch, f"*{target_current_branch}") for branch in
                                   node.branch]

    def find_node_by_checkout(self, nodes: List[Node], target_current_node: bool,
                              target_current_branch: str or None) -> Node or None:
        for node in nodes:
            if target_current_branch in node.branch:
                return node

            if node.currentNode == target_current_node and (
                    target_current_branch is None or node.currentBranch == target_current_branch):
                return node
            found_node = self.find_node_by_checkout(node.children, target_current_node, target_current_branch)
            if found_node:
                return found_node
        return None

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
