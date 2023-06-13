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


class Node(models.Model):
    COMMIT = 0
    BRANCH = 1

    TYPE_CHOICES = [
        (COMMIT, 'Commit'),
        (BRANCH, 'Branch')
    ]

    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=255, null=True)
    parent = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='children')
    type = models.IntegerField(choices=TYPE_CHOICES)
    task = models.ForeignKey(Task, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.id}"


class NodeSolve(models.Model):
    COMMIT = 0
    BRANCH = 1

    TYPE_CHOICES = [
        (COMMIT, 'Commit'),
        (BRANCH, 'Branch')
    ]

    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=255, null=True)
    parent = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='children')
    type = models.IntegerField(choices=TYPE_CHOICES)
    task = models.ForeignKey(Task, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.id}"


class RemoteNode(models.Model):
    COMMIT = 0
    BRANCH = 1

    TYPE_CHOICES = [
        (COMMIT, 'Commit'),
        (BRANCH, 'Branch')
    ]

    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=255, null=True)
    parent = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='children')
    type = models.IntegerField(choices=TYPE_CHOICES)
    task = models.ForeignKey(Task, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.id}"


class RemoteNodeSolve(models.Model):
    COMMIT = 0
    BRANCH = 1

    TYPE_CHOICES = [
        (COMMIT, 'Commit'),
        (BRANCH, 'Branch')
    ]

    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=255, null=True)
    parent = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='children')
    type = models.IntegerField(choices=TYPE_CHOICES)
    task = models.ForeignKey(Task, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.id}"
