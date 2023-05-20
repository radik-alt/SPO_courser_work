import json
import os

import git

import json_files
from django.core.management.base import BaseCommand
from git_branch.models import Task, Info, InfoDetail


class Command(BaseCommand):
    def handle(self):
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'task.json'))

        with open(file_path, encoding="UTF-8") as f:
            data = json.load(f)

            # Iterate over the tasks in the JSON data
            for task_data in data['tasks']:
                # Create a Task object
                task = Task(solve=task_data['solve'])
                task.save()

                # Iterate over the list_info_task in the task_data
                for info_data in task_data['list_info_task']:
                    # Create an Info object
                    info = Info(title=info_data['title'], task=task)
                    info.save()

                    # Iterate over the info in the info_data
                    for content in info_data['info']:
                        # Create an InfoDetail object
                        info_detail = InfoDetail(info=info, content=content)
                        info_detail.save()


repo = git.Repo('.')
commands = {}

git_cmd = repo.git
git_commands = git_cmd.execute(['help', '-a']).splitlines()

for command in git_commands:
    if not command.startswith(' '):
        command_name = command.split()[0]
        command_desc = ' '.join(command.split()[1:])
        commands[command_name] = command_desc

print(command)