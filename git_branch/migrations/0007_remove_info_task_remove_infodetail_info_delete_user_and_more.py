# Generated by Django 4.2 on 2023-05-17 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('git_branch', '0006_remove_task_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='info',
            name='task',
        ),
        migrations.RemoveField(
            model_name='infodetail',
            name='info',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.DeleteModel(
            name='Info',
        ),
        migrations.DeleteModel(
            name='InfoDetail',
        ),
        migrations.DeleteModel(
            name='Task',
        ),
    ]