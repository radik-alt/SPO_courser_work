from django.db import models


# Create your models here.
class Levels(models.Model):
    id_level = models.IntegerField()
    title_level = models.CharField(max_length=255)
    description = models.TextField()


class Tasks(models.Model):
    id_task = models.IntegerField()


class TaskList(models.Model):
    print()


