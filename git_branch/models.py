from django.db import models


class Levels(models.Model):
    title_level = models.CharField(max_length=100)
    image = models.ImageField(null=True, default=None)
    description = models.TextField()


class Task(models.Model):
    level = models.ForeignKey(Levels, on_delete=models.PROTECT, null=True)
    solve = models.BooleanField(default=False)


class Info(models.Model):
    title = models.CharField(max_length=255)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class InfoDetail(models.Model):
    info = models.ForeignKey(Info, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)

# class User(models.Model):
#     pass
