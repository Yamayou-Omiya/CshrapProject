import os
import json

workspace_folder = os.getcwd()

# launch.jsonテンプレート
launch_template = {
    "version": "0.2.0",
    "configurations": []
}

# tasks.jsonテンプレート
tasks_template = {
    "version": "2.0.0",
    "tasks": []
}

# プロジェクトディレクトリを検索
for folder_name in os.listdir(workspace_folder):
    folder_path = os.path.join(workspace_folder, folder_name)
    if os.path.isdir(folder_path) and os.path.exists(os.path.join(folder_path, f"{folder_name}.csproj")):
        # launch.jsonの設定を追加
        launch_template["configurations"].append({
            "name": f"{folder_name} .NET Core Launch (console)",
            "type": "coreclr",
            "request": "launch",
            "preLaunchTask": f"build {folder_name}",
            "program": f"${{workspaceFolder}}/{folder_name}/bin/Debug/net8.0/{folder_name}.dll",
            "args": [],
            "cwd": f"${{workspaceFolder}}/{folder_name}",
            "stopAtEntry": False,
            "console": "externalTerminal" if folder_name == "A01" else "internalConsole",
            "internalConsoleOptions": "openOnSessionStart",
            "launchBrowser": {
                "enabled": False
            },
            "env": {
                "ASPNETCORE_ENVIRONMENT": "Development"
            },
            "sourceFileMap": {
                "/Views": f"${{workspaceFolder}}/Views"
            }
        })

        # tasks.jsonの設定を追加
        tasks_template["tasks"].append({
            "label": f"build {folder_name}",
            "command": "dotnet",
            "type": "process",
            "args": [
                "build",
                f"${{workspaceFolder}}/{folder_name}/{folder_name}.csproj"
            ],
            "problemMatcher": "$msCompile"
        })

# launch.jsonファイルを書き込み
with open(os.path.join(workspace_folder, ".vscode", "launch.json"), 'w') as launch_file:
    json.dump(launch_template, launch_file, indent=4)

# tasks.jsonファイルを書き込み
with open(os.path.join(workspace_folder, ".vscode", "tasks.json"), 'w') as tasks_file:
    json.dump(tasks_template, tasks_file, indent=4)
    
print("launch.json と tasks.json が更新されました。")
