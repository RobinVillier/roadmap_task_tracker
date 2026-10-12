import argparse
import json
import datetime
from pathlib import Path


DEFAULT_DB = Path().cwd() / "database" / "tasks.json"

def load(db: Path) -> list[dict]:
    db.touch(exist_ok=True)

    try:
        task_list = json.loads(db.read_text())
    except json.decoder.JSONDecodeError:
        task_list = []

    return task_list


def save(db: Path, tasks: list[dict]):
    db.write_text(json.dumps(tasks, indent=2))


def add_task(args):
    tasks_list = load(args.db)

    new_task = {
        "title": args.title,
        "status": args.status,
        "created": str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    }

    tasks_list.append(new_task)

    save(db=args.db, tasks=tasks_list)


def update_task(args):
    tasks_list = load(args.db)

    tasks_list[int(args.index) - 1]["title"] = args.title

    save(db=args.db, tasks=tasks_list)

def update_status(args):
    tasks_list = load(args.db)

    tasks_list[int(args.index) - 1]["status"] = args.status

    save(db=args.db, tasks=tasks_list)


def delete_task(args):
    tasks_list = load(args.db)

    del tasks_list[int(args.index )- 1]

    save(db=args.db, tasks=tasks_list)


def list_tasks(args):
    mode = args.mode
    tasks_list = load(args.db)

    for index, task in enumerate(tasks_list, start=1):
        if mode == "all" or task["status"] == mode:
            print(f"{index:02d} - {task['title']} - {task['created']} - {task['status']}")
        

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='tasks', description='CLI Task Tracker with argparser')

    parser.add_argument('--db', type=Path, default=DEFAULT_DB, help=f"Task file (default: {DEFAULT_DB})")

    sub = parser.add_subparsers(dest='command', required=True)

    p = sub.add_parser("add", help="Add a task.")
    p.add_argument("title")
    p.add_argument("-s", "--status", choices=["done", "not done", "in progress"], default="not done")
    p.set_defaults(func=add_task)

    p = sub.add_parser("update", help="Update a task.")
    p.add_argument("index")
    p.add_argument("title")
    p.add_argument("-s", "--status", choices=["done", "not done", "in progress"], default="not done")
    p.set_defaults(func=update_task)

    p = sub.add_parser("delete", help="Delete a task.")
    p.add_argument("index")
    p.set_defaults(func=delete_task)

    p = sub.add_parser("update-status", help="Update a task status.")
    p.add_argument("index")
    p.add_argument("-s", "--status", choices=["done", "not done", "in progress"], default="not done")
    p.set_defaults(func=update_status)

    p = sub.add_parser("list-tasks", help="Lists task depeding on the mode.")
    p.add_argument("-m", "--mode", choices=["all", "done", "not done", "in progress"], default="all")
    p.set_defaults(func=list_tasks)

    return parser


if __name__ == "__main__": 
    args = build_parser().parse_args()
    args.func(args)  # dispatch to the subcommand's handler
