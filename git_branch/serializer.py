from rest_framework import serializers

from git_branch.models import Levels, Task, InfoDetail, Info


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