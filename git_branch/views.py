import logging
import traceback
from collections import deque
from typing import List

from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
import json
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
        self.visible = True

    def __str__(self):
        return f"Node(id={self.id} name={self.name}, parent={self.parent}, children={self.children}, " \
               f"branch={self.branch}, currentBranch={self.currentBranch}, currentNode={self.currentNode})"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "parent": [node_id for node_id in self.parent],
            "children": [node.to_dict() for node in self.children],
            "branch": self.branch,
            "currentBranch": self.currentBranch,
            "currentNode": self.currentNode
        }

    @classmethod
    def from_dict(cls, data):
        node = cls()
        node.id = data.get("id", "")
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
        self.task_id = -1


class SolveGraphApi(APIView):

    def __pos__(self, request):
        # graph: List[Node] = self.parse_data(request.data.get("data", []))
        # task_id = request.data.get("task_id", -1)

        return Response({
            "solve": False,
            "result": 0,
            "message": "Проверка решение задачи!"
        })


class WorkGraph(APIView):

    def post(self, request):

        self.all_node = []

        try:
            data_dict = request.data
            print(type(data_dict))

            model = Model()
            model.data: List[Node] = self.parse_data(data_dict.get("data", []))
            model.command = data_dict.get("command", "")
            model.task_id = data_dict.get("task_id", "")

            remote_allow = False
            remote_nodes: List[Node] = model.data

            self.print_tree(model.data[0])

            status = 0
            message = "Success"

            if self.valid(command=model.command):
                _commad = model.command.split()

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

                elif _commad[1] == "rebase":
                    name = self.get_name(model.command)
                    self.rebase(model.data, name)

                elif _commad[1] == "merge":
                    name = self.get_name(model.command)
                    self.merge(model.data, name)

                elif _commad[1] == "cherry-pick":
                    name_commit = self.get_name_commit_cherry_pick(_commad)
                    self.cherry_pick(model.data, name_commit)

                elif _commad[1] == "reset":
                    self.reset_commit()

                elif _commad[1] == "revert":
                    depth = self.revert_count_commit(_commad)
                    nodes = model.data
                    checkout_node = self.find_node_by_checkout(nodes, True, None)
                    self.revert_commit(nodes[0], checkout_node, depth)

                elif _commad[1] == "push":
                    remote_allow = True
                    remote_nodes = model.data

                elif _commad[1] == "clone":
                    remote_allow = True
                    remote_nodes = model.data

                elif _commad[1] == "fetch":
                    remote_allow = True
                    remote_nodes = model.data


            else:
                raise Exception()
        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")
            response = Response(
                {
                    "data": None,
                    "remote_data": None,
                    "message": "Ошибка! Проверьте правильно написана ли ваша команда",
                    "code": -1
                })
            response.status_code = 200
            return response

        # self.print_tree(model.data)
        serialized_nodes = json.dumps([node.to_dict() for node in model.data])
        # print(serialized_nodes)

        serialized_nodes_remote = None
        if remote_allow:
            serialized_nodes_remote = json.dumps([node.to_dict() for node in remote_nodes])

        return Response({
            "data": serialized_nodes,
            "remote_data": serialized_nodes_remote,
            "message": message,
            "code": status})

    def revert_count_commit(self, commands) -> int:
        return int(commands[2][-1])

    def get_name_commit_cherry_pick(self, commands: List[str]) -> List[str]:
        try:
            name_commit = []
            for index, command in enumerate(commands):
                if index > 1:
                    name_commit.append(command)

            return name_commit
        except Exception as e:
            traceback.print_exc()
            return []

    def print_tree(self, root):
        if not root:
            return

        queue = deque([(root, 0)])

        while queue:
            node, level = queue.popleft()
            self.all_node.append(node)
            # print("  " * level, end="")
            # print(node)
            for child in node.children:
                queue.append((child, level + 1))

    def revert_commit(self, node: Node, checkout_node: Node, depth: int):
        prev_node: Node = self.find_prev_node(node, checkout_node.id, depth)
        prev_node.children.remove(checkout_node)

    def find_prev_node(self, node: Node, parent_id: int, depth: int):
        parent_node_select = self.get_parent_id_node(node, parent_id)
        if depth == 0:
            return parent_node_select

        for parent in parent_node_select.parent:
            change_depth = depth - 1
            result = self.find_prev_node(parent_node_select, parent, change_depth)
            if result is not None:
                return result

    def get_parent_id_node(self, nodes: Node, id: int):
        if nodes.id == id:
            return nodes

        for node in nodes.children:
            if node:
                result = self.get_parent_id_node(node, id)
                if result is not None:
                    return result

    def reset_commit(self):
        pass

    def get_name_checkout_node(self, name):
        return f"*{name}"

    def convert_node_to_dict(self, node: Node):
        node_dict = {
            "name": node.name,
            "parent": [],
            "children": [self.convert_node_to_dict(child) for child in node.children] if node.children else [],
            "branch": node.branch,
            "currentBranch": node.currentBranch,
            "currentNode": node.currentNode
        }
        return node_dict

    def cherry_pick(self, nodes: List[Node], commit_list: List[str]):
        for commit in commit_list:
            checkout_node = self.find_node_by_checkout(nodes, True, None)
            print(checkout_node)
            copy_node = self.find_commit_by_name(nodes[0], commit)
            print(f"Copy: {copy_node}")
            self.add_copy_commit(checkout_node, copy_node)
            self.change_checkout_cherry_pick(checkout_node, copy_node)

    def change_checkout_cherry_pick(self, checkout_node: Node, new_node: Node):
        new_node.currentNode = checkout_node.currentNode
        new_node.branch.append(self.get_name_checkout_node(checkout_node.currentBranch))
        new_node.currentBranch = checkout_node.currentBranch
        self.clear_branch_data_checkout(checkout_node)

    def add_copy_commit(self, node: Node, copy_node: Node):
        try:
            if not node.children:
                node.children.append(copy_node)
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()

    def find_commit_by_name(self, node: Node, name: str) -> Node or None:
        if node.name == name:
            return node

        for child in node.children:
            if child:
                result = self.find_commit_by_name(child, name)
                if result is not None:
                    return result

        return None

    def rebase(self, nodes: List[Node], name: str):
        node = self.find_node_by_checkout(nodes, True, None)
        origin = self.find_last_node_by_branch(nodes[0], name)

        print("Rebase")
        print(f"Checkout: {node}")
        print(f"Branch {name}: {origin}")

        top_bottom = self.valid_rebase_top_to_down(node, origin)
        bottom_top = self.valid_rebase_top_to_down(origin, node)

        print(top_bottom)
        print(bottom_top)

        if bottom_top:
            node.branch.append(origin.currentBranch)
            origin.branch.clear()
            origin.currentBranch = ""
        elif top_bottom:
            return
        else:
            parent_node: Node = self.find_node_by_id(nodes[0], node.parent[0])
            print(parent_node)
            find_node_remove = self.remove_children_rebase(parent_node.children, node.id)
            parent_node.children.remove(find_node_remove)
            origin.children.append(find_node_remove)
            self.change_to_rebase_commit(find_node_remove)

    def remove_children_rebase(self, nodes: List[Node], id: int) -> Node:
        for index, node in enumerate(nodes):
            print(node)
            if node.id == id:
                return node

    def find_parent(self, nodes: List[Node], parend_id: int):
        for node in nodes:
            if len(node.children) > 1 and node.id == parend_id:
                return node

    def change_to_rebase_commit(self, node: Node):
        if node is None:
            return

        node.name = self.set_rebase_commit(node.name)
        for child in node.children:
            if child:
                self.change_to_rebase_commit(child)

    def set_rebase_commit(self, name: str):
        return f"{name}'"

    def find_node_by_id(self, node, target_id):
        if node.id == target_id:
            return node

        for child_node in node.children:
            found_node = self.find_node_by_id(child_node, target_id)
            if found_node is not None:
                return found_node

        return None

    def add_branch_rebase(self, node: Node, checkout_node: Node):
        node.branch = []
        if node.currentBranch:
            checkout_node.branch.append(str(node.currentBranch))
        node.currentBranch = ""

    def valid_rebase_top_to_down(self, branch_one: Node, branch_two) -> bool:
        for node in branch_one.children:

            if node.children:
                if branch_two in node.children:
                    return True
                self.valid_rebase_top_to_down(node.children, branch_two)
            else:
                return False

    def merge(self, nodes: List[Node], name: str):
        node = self.find_node_by_checkout(nodes, True, None)
        if not name == node.currentBranch:
            origin = self.find_last_node_by_branch(nodes[0], name)

            new_id = self.find_max_id(nodes)
            merge = self.merge_nodes(node, origin, new_id)
            merge.parent.append(node.id)
            merge.parent.append(origin.id)
            other_merge = self.merge_nodes(node, origin, new_id)

            self.clear_branch_data_checkout(other_merge)
            # origin.children.append(other_merge)

            self.clear_branch_data_checkout(node)
            node.children.append(merge)

        else:
            raise Exception()

    def merge_nodes(self, node1: Node, node2: Node, id: int) -> Node:
        merged_node = Node()
        merged_node.id = id + 1
        merged_node.name = f"C{id + 1}"
        merged_node.children = []
        merged_node.parent = []
        merged_node.branch.append(self.get_name_checkout_node(node1.currentBranch))
        merged_node.currentBranch = node1.currentBranch
        merged_node.currentNode = node1.currentNode
        merged_node.type = 2
        return merged_node

    def clear_nodes_data_merge(self, node1: Node, node2: Node):
        pass

    def clear_branch_data(self, node: Node):
        node.branch.remove(node.currentBranch)
        node.currentNode = False
        if node.branch:
            node.currentBranch = node.branch[0]
        else:
            node.currentBranch = ""

    def clear_branch_data_checkout(self, node: Node):
        node.branch.remove(self.get_name_checkout_node(node.currentBranch))
        node.currentNode = False
        if node.branch:
            node.currentBranch = node.branch[0]
        else:
            node.currentBranch = ""

    def commit(self, nodes: List[Node]):
        node = self.find_node_by_checkout(nodes, True, None)
        print(node)
        new_id = self.find_max_id(nodes)
        new_commit = self.create_node(id=new_id + 1, name=f"C{new_id + 1}", parent=[], children=[],
                                      branch=[self.get_name_checkout_node(node.currentBranch)],
                                      current_branch=node.currentBranch, current_node=True)
        node.branch.remove(self.get_name_checkout_node(node.currentBranch))
        node.currentBranch = ""
        node.currentNode = False

        new_commit.parent.append(node.id)
        node.children.append(new_commit)

    def find_max_id(self, nodes: List[Node]):
        max_id = -1

        for node in nodes:
            max_id = max(max_id, node.id)

            if node.children:
                max_id = max(max_id, self.find_max_id(node.children))

        return max_id

    def find_last_node_by_branch(self, node: Node, target_current_branch: str) -> Node or None:
        if node.currentBranch == target_current_branch:
            return node

        last_node = None
        for child in node.children:
            child_node = self.find_last_node_by_branch(child, target_current_branch)
            if child_node:
                last_node = child_node

        return last_node

    def create_node(self, id: int, name: str, parent: [], children: [], branch: List[str] or None, current_branch: str,
                    current_node: bool):
        node = Node()
        node.id = id
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
        return ["commit", "push", "branch", "checkout", "pull", "clone", "fetch", "merge", "rebase", "cherry-pick",
                "revert", "reset"]

    def valid(self, command) -> bool:
        split_list = command.split()
        first_word = split_list[0]
        second_word = split_list[1]
        return first_word == "git" and second_word in self.all_commands()

    def parse_data(self, data: List[dict]) -> List[Node]:
        nodes = []
        data_list = [data]
        try:
            for item in data_list:
                node = Node()
                node.id = item.get("id", -1)
                node.name = item.get('name', "")
                node.parent = item.get('parent', [])
                node.children = self.parse_nodes(item.get('children', []))
                node.branch = item.get('branch', [])
                node.currentBranch = item.get('currentBranch', "")
                node.currentNode = item.get('currentNode', False)

                nodes.append(node)
        except Exception as e:
            print("Ошибка парсинга блядь!")
            print(f"Произошла ошибка: {e}")
            traceback.print_exc()

        return nodes

    def parse_nodes(self, nodes: List[dict]) -> List[Node]:
        parsed_nodes = []

        try:
            for item in nodes:
                node = Node()
                node.id = item.get("id", -1)
                node.name = item.get('name', "")
                node.parent = item.get('parent', [])
                node.children = self.parse_nodes(item.get('children', []))
                node.branch = item.get('branch', [])
                node.currentBranch = item.get('currentBranch', "")
                node.currentNode = item.get('currentNode', False)

                parsed_nodes.append(node)
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()

        return parsed_nodes

    def add_branch(self, nodes: List[Node], target_current_branch: str):
        for node in nodes:
            if node.currentNode:
                node.branch.append(target_current_branch)
            self.add_branch(node.children, target_current_branch)
            # self.update_current_node(node.children, target_current_branch)

    def update_current_node(self, nodes: List[Node], target_current_branch: str):
        for node in nodes:
            self.change_checkout_data_to_false(node)

            if target_current_branch in node.branch:
                self.change_checkout_into_one_node(node, target_current_branch)
            elif node.currentBranch == target_current_branch:
                if not node.children:
                    self.change_checkout_data_to_true(node, target_current_branch)
            elif len(node.branch) == 0:
                node.currentBranch = ""

            self.update_current_node(node.children, target_current_branch)

    def change_checkout_data_to_false(self, node: Node):
        node.currentNode = False  # Установка значения currentNode в False для всех узлов
        node.branch = [branch.replace(self.get_name_checkout_node(node.currentBranch), node.currentBranch) for
                       branch in
                       node.branch]
        node.currentBranch = node.currentBranch

    def change_checkout_data_to_true(self, node: Node, target_current_branch: str):
        node.currentBranch = target_current_branch
        node.currentNode = True
        node.branch = [branch.replace(target_current_branch, f"*{target_current_branch}") for branch in
                       node.branch]

    def change_checkout_into_one_node(self, node: Node, target_current_branch: str):
        node.currentBranch = target_current_branch
        node.currentNode = True
        node.branch = [branch.replace(self.get_name_checkout_node(node.currentBranch), node.currentBranch) for
                       branch in
                       node.branch]
        node.branch = [branch.replace(target_current_branch, f"*{target_current_branch}") for branch in
                       node.branch]

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
