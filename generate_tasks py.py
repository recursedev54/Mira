import os
import json

workspace_folder = os.getcwd()  # Assuming this script is run from the root of the workspace
tasks = {
    "version": "2.0.0",
    "tasks": []
}

for root, dirs, files in os.walk(workspace_folder):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            task = {
                "label": f"Run {file}",
                "type": "shell",
                "command": "python",
                "args": [
                    file_path
                ],
                "group": {
                    "kind": "build",
                    "isDefault": False
                },
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": True,
                    "panel": "new"
                },
                "problemMatcher": []
            }
            tasks["tasks"].append(task)

vscode_dir = os.path.join(workspace_folder, '.vscode')
os.makedirs(vscode_dir, exist_ok=True)
tasks_file = os.path.join(vscode_dir, 'tasks.json')

with open(tasks_file, 'w') as f:
    json.dump(tasks, f, indent=4)

print(f"tasks.json generated at {tasks_file}")
