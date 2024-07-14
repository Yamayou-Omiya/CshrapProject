# はじめに
VSCodeでC#のプロジェクトを作ったときに，複数C#のプロジェクトが存在すると実行してくれない問題を解決するために試行錯誤したので備忘録として残しておきます．
ここでは，プロジェクトを指定してデバッグする方法を実践しています．

# 環境
OS: Windows11
VSCode 1.90.2
VSCodeの拡張機能（C# Dev Kit）
.NET 8.0

# 方法
結論から言うとlaunch.jsonとtasks.jsonを作成していい感じに設定してあげれば良い

まず以下のような状態を想定する．Projectというフォルダの中にそれぞれProject1，Project2というC#プロジェクトが存在する．
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3817552/b810d076-8864-8748-7a6a-06fcb5a1e18a.png)

## launch.jsonの設定
サイドバーの実行とデバッグから「launch.jsonファイルを作成します」をクリックし，C#を選択する．
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3817552/bddbb6e2-391f-5a0a-b636-e8af45c284f8.png)
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3817552/25062221-ac0a-3e58-1d5d-f9df4b5bfb0a.png)

launch.jsonの中身を以下のように変更する．私もlaunchの中身はよくわからないので多分不要な項目も結構混じってると思う．詳しい人はどんどん削っていってください．

```json:launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "project1 .NET Core Launch (console)",
            "type": "coreclr",
            "request": "launch",
            "preLaunchTask": "build project1",
            "program": "${workspaceFolder}/project1/bin/Debug/net8.0/project1.dll",
            "args": [],
            "cwd": "${workspaceFolder}/project1",
            "stopAtEntry": false,
            "console": "internalConsole",
            "internalConsoleOptions": "openOnSessionStart",
            "launchBrowser": {
                "enabled": false
            },
            "env": {
                "ASPNETCORE_ENVIRONMENT": "Development"
            },
            "sourceFileMap": {
                "/Views": "${workspaceFolder}/Views"
            }
        },
        {
            "name": "project2 .NET Core Launch (console)",
            "type": "coreclr",
            "request": "launch",
            "preLaunchTask": "build project2",
            "program": "${workspaceFolder}/project2/bin/Debug/net8.0/project2.dll",
            "args": [],
            "cwd": "${workspaceFolder}/project2",
            "stopAtEntry": false,
            "console": "internalConsole",
            "internalConsoleOptions": "openOnSessionStart",
            "launchBrowser": {
                "enabled": false
            },
            "env": {
                "ASPNETCORE_ENVIRONMENT": "Development"
            },
            "sourceFileMap": {
                "/Views": "${workspaceFolder}/Views"
            }
        }
    ]
}

```

## tasks.jsonの作成
続いてビルドタスクを設定していく．以下のようになるようにtasks.jsonを作成してあげる．
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3817552/8666a4fd-84d0-1945-4b6d-494b907f5c88.png)

tasks.jsonの中身を以下のように設定する．詳しい人はどんどん削ってください．
```json:tasks.json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "build project1",
            "command": "dotnet",
            "type": "process",
            "args": [
                "build",
                "${workspaceFolder}/project1/project1.csproj"
            ],
            "problemMatcher": "$msCompile"
        },
        {
            "label": "build project2",
            "command": "dotnet",
            "type": "process",
            "args": [
                "build",
                "${workspaceFolder}/project2/project2.csproj"
            ],
            "problemMatcher": "$msCompile"
        }
    ]
}
```
これで保存すると以下のように実行とデバッグの欄からproject1とproject2が選べるようになっているはず．実行したいプロジェクトを選択してF5を押せばデバッグができるようになる．
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3817552/9557758d-0938-24aa-fb93-1f170a04ea4f.png)

# launch.jsonとtasks.jsonを自動更新する
毎回手打ちするのは大変なので，自動でjsonファイルを更新するコードをchatGPTに書いてもらったのでここに乗せておく

```Python:update_vscode_configs.py
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

```


# おまけ
"console": "internalConsole",の部分を"console": "externalTerminal",に変えるとコンソール画面が出てくるようになるよ
