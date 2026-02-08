"""JSON persistence layer for task storage."""
import json
import os
from datetime import datetime
from typing import List, Dict, Any


class TaskStorage:
    """Handles saving and loading tasks from JSON file."""
    
    def __init__(self, data_file: str = None):
        """Initialize storage with optional custom data file path."""
        if data_file is None:
            # Store in user's home directory under .task-tracker
            home_dir = os.path.expanduser("~")
            self.data_dir = os.path.join(home_dir, ".task-tracker")
            self.data_file = os.path.join(self.data_dir, "tasks.json")
        else:
            self.data_file = data_file
            self.data_dir = os.path.dirname(data_file)
        
        # Ensure directory exists
        os.makedirs(self.data_dir, exist_ok=True)
    
    def load_tasks(self) -> List[Dict[str, Any]]:
        """Load tasks from JSON file. Returns empty list if file doesn't exist."""
        if not os.path.exists(self.data_file):
            return []
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    
    def save_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        """Save tasks to JSON file."""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=2, default=str)
    
    def get_next_id(self, tasks: List[Dict[str, Any]]) -> int:
        """Get the next available task ID."""
        if not tasks:
            return 1
        return max(task.get('id', 0) for task in tasks) + 1
