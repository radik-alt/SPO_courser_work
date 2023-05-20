# Generated by Django 4.2 on 2023-05-17 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('git_branch', '0004_alter_task_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='levels',
            name='image',
            field=models.ImageField(default=None, upload_to=''),
        ),
        migrations.AlterField(
            model_name='task',
            name='level',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Tasks', to='git_branch.levels'),
        ),
    ]
