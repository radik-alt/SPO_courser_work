# Generated by Django 4.2 on 2023-06-05 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('git_branch', '0011_node'),
    ]

    operations = [
        migrations.CreateModel(
            name='RemoteNodeSolve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.IntegerField(choices=[(0, 'Commit'), (1, 'Branch')])),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='git_branch.remotenodesolve')),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='git_branch.task')),
            ],
        ),
        migrations.CreateModel(
            name='RemoteNode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.IntegerField(choices=[(0, 'Commit'), (1, 'Branch')])),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='git_branch.remotenode')),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='git_branch.task')),
            ],
        ),
        migrations.CreateModel(
            name='NodeSolve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.IntegerField(choices=[(0, 'Commit'), (1, 'Branch')])),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='git_branch.nodesolve')),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='git_branch.task')),
            ],
        ),
    ]
