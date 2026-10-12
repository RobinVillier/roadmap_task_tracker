# Description

I was browsing [roadmap.sh](https://roadmap.sh/python) today and came across a few Python features I hadn’t used before, like argparse subcommands and dispatching each one to its own handler. Mainly due to my tech anim background, and I really want it to change. 
Rather than just reading about them, I wanted to try them out right away, so I picked a simple project from the site, the [Task Tracker](https://roadmap.sh/projects/task-tracker), and built it as a small sandbox to put them into practice.

I also wanted to startup a project with poetry, after also reading about it today, even if this project doesnt have any dependencies, I gave it a try, gathered some notes on it, and I am ready to use it again on more complex projects.

## Tasks - CLI Task Tracker

A small command-line task tracker built with Python's `argparse`. Tasks are stored in a local JSON file.

### Requirements

- Python 3.9+
- No external dependencies

## Setup

By default, tasks are stored in `./database/tasks.json` (relative to the directory you run the command from). Create the folder before the first run:

```bash
mkdir database
```

The JSON file itself is created automatically.

## Usage

```bash
python tasks.py [--db PATH] <command> [options]
```

| Option | Description |
|---|---|
| `--db PATH` | Use a different task file (default: `./database/tasks.json`) |

### Commands

**Add a task**
```bash
python tasks.py add "Buy groceries"
python tasks.py add "Write report" -s "in progress"
```

**List tasks**
```bash
python tasks.py list-tasks            # all tasks
python tasks.py list-tasks -m done    # filter by status
python tasks.py list-tasks -m "in progress"
```
Output for all tasks:
```
01 - Buy groceries - 2026-10-12 22:14:46 - not done
02 - Write report - 2026-10-12 22:15:10 - in progress
```

**Rename a task**
```bash
python tasks.py update 1 "Buy groceries and milk"
```

**Change a task's status**
```bash
python tasks.py update-status 2 -s done
```

**Delete a task**
```bash
python tasks.py delete 1
```

Tasks are referenced by the 1-based index shown in `list-tasks`. Note that indexes shift after a deletion.

### Statuses

`not done` (default) · `in progress` · `done`

Statuses containing a space must be quoted: `-s "not done"`.

## Data format

```json
[
  {
    "title": "Buy groceries",
    "status": "not done",
    "created": "2026-10-12 22:14:46"
  }
]
```
