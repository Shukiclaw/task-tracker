"""Core task management logic."""
from datetime import datetime
from typing import List, Dict, Any, Optional
from storage import TaskStorage


class TaskManager:
    """Manages task operations and business logic."""
    
    PRIORITIES = {"high": 3, "medium": 2, "low": 1}
    
    def __init__(self, storage: TaskStorage = None):
        """Initialize with optional custom storage."""
        self.storage = storage or TaskStorage()
        self._tasks = None
    
    @property
    def tasks(self) -> List[Dict[str, Any]]:
        """Lazy load tasks from storage."""
        if self._tasks is None:
            self._tasks = self.storage.load_tasks()
        return self._tasks
    
    def _save(self) -> None:
        """Persist current tasks to storage."""
        self.storage.save_tasks(self._tasks)
    
    def add_task(self, title: str, priority: str = "medium", 
                 description: str = "") -> Dict[str, Any]:
        """Add a new task with given title and priority."""
        # Normalize priority
        priority = priority.lower()
        if priority not in self.PRIORITIES:
            priority = "medium"
        
        task = {
            "id": self.storage.get_next_id(self.tasks),
            "title": title,
            "description": description,
            "priority": priority,
            "completed": False,
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
        }
        
        self.tasks.append(task)
        self._save()
        return task
    
    def get_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Get a task by ID."""
        for task in self.tasks:
            if task.get("id") == task_id:
                return task
        return None
    
    def list_tasks(self, status: str = None, priority: str = None) -> List[Dict[str, Any]]:
        """List tasks with optional filtering."""
        result = self.tasks.copy()
        
        # Filter by status
        if status == "completed":
            result = [t for t in result if t.get("completed")]
        elif status == "pending":
            result = [t for t in result if not t.get("completed")]
        
        # Filter by priority
        if priority and priority.lower() in self.PRIORITIES:
            result = [t for t in result if t.get("priority") == priority.lower()]
        
        # Sort by priority (high first), then by ID
        result.sort(key=lambda t: (
            -self.PRIORITIES.get(t.get("priority", "medium"), 2),
            t.get("id", 0)
        ))
        
        return result
    
    def complete_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Mark a task as completed."""
        task = self.get_task(task_id)
        if task:
            task["completed"] = True
            task["completed_at"] = datetime.now().isoformat()
            self._save()
        return task
    
    def uncomplete_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Mark a task as not completed (reopen)."""
        task = self.get_task(task_id)
        if task:
            task["completed"] = False
            task["completed_at"] = None
            self._save()
        return task
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID. Returns True if deleted."""
        for i, task in enumerate(self.tasks):
            if task.get("id") == task_id:
                self.tasks.pop(i)
                self._save()
                return True
        return False
    
    def update_task(self, task_id: int, title: str = None, 
                    description: str = None, priority: str = None) -> Optional[Dict[str, Any]]:
        """Update task fields."""
        task = self.get_task(task_id)
        if not task:
            return None
        
        if title is not None:
            task["title"] = title
        if description is not None:
            task["description"] = description
        if priority is not None and priority.lower() in self.PRIORITIES:
            task["priority"] = priority.lower()
        
        self._save()
        return task
    
    def get_stats(self) -> Dict[str, int]:
        """Get task statistics."""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.get("completed"))
        pending = total - completed
        
        by_priority = {"high": 0, "medium": 0, "low": 0}
        for task in self.tasks:
            p = task.get("priority", "medium")
            if p in by_priority and not task.get("completed"):
                by_priority[p] += 1
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "high_priority": by_priority["high"],
            "medium_priority": by_priority["medium"],
            "low_priority": by_priority["low"],
        }
    
    def clear_completed(self) -> int:
        """Remove all completed tasks. Returns count removed."""
        original_count = len(self.tasks)
        self._tasks = [t for t in self.tasks if not t.get("completed")]
        removed = original_count - len(self._tasks)
        if removed > 0:
            self._save()
        return removed
