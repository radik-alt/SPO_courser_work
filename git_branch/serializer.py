from rest_framework import serializers

from git_branch.models import Levels, Task, InfoDetail, Info, Node, NodeSolve


class LevelsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Levels
        fields = "__all__"


class InfoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoDetail
        fields = ('info', 'content')

class InfoSerializer(serializers.ModelSerializer):
    infodetail_set = InfoDetailSerializer(many=True)

    class Meta:
        model = Info
        fields = ('title', 'infodetail_set')

class TaskSerializer(serializers.ModelSerializer):
    info_set = InfoSerializer(many=True)

    class Meta:
        model = Task
        fields = ('id', 'level', 'solve', 'info_set')


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["solve"]


class NodeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Node
        fields = ['id', 'name', 'parent', 'type', 'children']

    def get_children(self, obj):
        # Рекурсивно сериализуем дочерние узлы
        children = obj.children.all()
        serializer = NodeSerializer(children, many=True)
        return serializer.data

class NodeSolveSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = NodeSolve
        fields = ['id', 'name', 'parent', 'type', 'children']

    def get_children(self, obj):
        # Рекурсивно сериализуем дочерние узлы
        children = obj.children.all()
        serializer = NodeSolveSerializer(children, many=True)
        return serializer.data