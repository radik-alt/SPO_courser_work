from django.db import models


class Levels(models.Model):
    title_level = models.CharField(max_length=100)
    image = models.ImageField(null=True, default=None)
    description = models.TextField()

    def __str__(self):
        return f"{self.title_level}"

    class Meta:
        ordering = ["id"]


class Task(models.Model):
    level = models.ForeignKey(Levels, on_delete=models.PROTECT, null=True)
    solve = models.BooleanField(default=False)

    def __str__(self):
        return f"Задача {self.id}"



class Info(models.Model):
    title = models.CharField(max_length=255)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"Info {self.id}"

class InfoDetail(models.Model):
    info = models.ForeignKey(Info, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Content {self.id}"

# class User(models.Model):
#     pass
