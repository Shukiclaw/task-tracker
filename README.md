# 📝 Task Tracker CLI

A beautiful, feature-rich command-line task management application built with Python, Click, and Rich.

## Features

- ✅ Add tasks with priority levels (high/medium/low)
- 📋 List tasks with filtering by status and priority
- ✏️ Update task details
- ✅ Mark tasks as complete/incomplete
- 🗑️ Delete tasks with confirmation
- 📊 View task statistics
- 🧹 Clear all completed tasks
- 💾 Persistent JSON storage
- 🎨 Colorful terminal output

## Installation

### From source (development mode):

```bash
git clone https://github.com/Shukiclaw/task-tracker.git
cd task-tracker
pip install -e .
```

### Requirements

- Python 3.8+
- click >= 8.0.0
- rich >= 13.0.0

## Usage

The CLI provides two command aliases:
- `task-tracker` - Full command name
- `tt` - Short alias

### Quick Start

```bash
# Add a new task
tt add "Finish the project report" -p high

# Add with description
tt add "Buy groceries" -p medium -d "Milk, eggs, bread"

# List all tasks
tt list

# Show only pending high priority tasks
tt list -s pending -p high

# Mark task as complete
tt complete 1

# Reopen a task
tt uncomplete 1

# Update a task
tt update 1 -t "Updated title" -p low

# Delete a task
tt delete 1

# View statistics
tt stats

# Clear all completed tasks
tt clear-completed
```

### Commands Reference

| Command | Description |
|---------|-------------|
| `add TITLE` | Add a new task |
| `list` | List all tasks |
| `complete ID` | Mark task as done |
| `uncomplete ID` | Reopen a task |
| `update ID` | Update task details |
| `delete ID` | Delete a task |
| `stats` | Show statistics |
| `clear-completed` | Remove all completed |

### List Filters

```bash
# By status
tt list -s completed   # Only completed
tt list -s pending     # Only pending
tt list -s all         # All (default)

# By priority
tt list -p high
tt list -p medium
tt list -p low

# Combined
tt list -s pending -p high
```

## Project Structure

```
task-tracker/
├── main.py           # CLI entry point (Click commands)
├── task_manager.py   # Core business logic
├── storage.py        # JSON persistence layer
├── setup.py          # Package installation config
├── requirements.txt  # Dependencies
└── README.md         # This file
```

## Data Storage

Tasks are stored in `~/.task-tracker/tasks.json` by default. Each task includes:

```json
{
  "id": 1,
  "title": "Task title",
  "description": "Optional description",
  "priority": "high|medium|low",
  "completed": false,
  "created_at": "2024-01-15T10:30:00",
  "completed_at": null
}
```

## Development

```bash
# Install in editable mode
pip install -e .

# Run tests
python -m pytest tests/

# Run directly without installing
python main.py add "Test task" -p high
```

## License

MIT License - Feel free to use and modify!

---

Built with ❤️ using [Click](https://click.palletsprojects.com/) and [Rich](https://rich.readthedocs.io/)
