from rest_framework import serializers

from git_branch.models import Levels


class LevelsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Levels
        fields = ('title_level', 'description')

