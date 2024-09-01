from typing import Optional

from typing_extensions import Annotated

import typer
import os
import json
from datetime import datetime

TODO_FILE_PATH = './todo_list.json'
tasks = []
app = typer.Typer()


@app.command()
def add(description: str):
    global tasks
    new_task = {
        "id": len(tasks) + 1,
        "description": description,
        "status": "todo",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    tasks.append(new_task)
    write_to_json_file()


@app.command()
def update(id: int, description: str):
    global tasks
    if not is_valid_id(id):
        return
    else:
        tasks[id - 1]["description"] = description
        tasks[id - 1]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        write_to_json_file()


@app.command()
def delete(id: int):
    global tasks
    if not is_valid_id(id):
        return
    else:
        tasks.pop(id - 1)
        for i in range(id - 1, len(tasks)):
            tasks[i]["id"] = i + 1
        write_to_json_file()


@app.command()
def mark_in_progress(id: int):
    global tasks
    if not is_valid_id(id):
        return
    else:
        tasks[id - 1]["status"] = "in-progress"
        write_to_json_file()


@app.command()
def mark_done(id: int):
    global tasks
    if not is_valid_id(id):
        return
    else:
        tasks[id - 1]["status"] = "done"
        write_to_json_file()


@app.command()
def list(status_type: Annotated[Optional[str], typer.Argument()] = None):
    print("[description - status - id]")
    for task in tasks:
        task_description = task["description"]
        task_status = task["status"]
        task_id = task["id"]
        task_output = f"{task_description} - {task_status} - {task_id}"
        if status_type is None:
            print(task_output)
        elif status_type == task_status == "done":
            print(task_output)
        elif status_type == task_status == "todo":
            print(task_output)
        elif status_type == task_status == "in-progress":
            print(task_output)


def is_valid_id(id: int):
    if id > len(tasks) or id < 1:
        print(f"Task with id {id} not found.")
        return False
    return True


def write_to_json_file():
    global tasks
    with open(TODO_FILE_PATH, "w") as file:
        json.dump({"tasks": tasks}, file)


def load_or_create_todo_list():
    global tasks

    if os.path.exists(TODO_FILE_PATH):
        with open(TODO_FILE_PATH, "r") as file:
            tasks = json.load(file)["tasks"]
    else:
        with open(TODO_FILE_PATH, "w") as file:
            json.dump({"tasks": []}, file)


if __name__ == "__main__":
    load_or_create_todo_list()
    app()
