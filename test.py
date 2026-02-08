#!/usr/bin/env python3
"""Test suite for Task Tracker CLI."""
import os
import sys
import tempfile
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from storage import TaskStorage
from task_manager import TaskManager


def test_storage():
    """Test JSON storage operations."""
    print("Testing Storage...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "test_tasks.json")
        storage = TaskStorage(data_file)
        
        # Test empty load
        tasks = storage.load_tasks()
        assert tasks == [], "Empty storage should return empty list"
        
        # Test save and load
        test_tasks = [
            {"id": 1, "title": "Test", "priority": "high", "completed": False}
        ]
        storage.save_tasks(test_tasks)
        loaded = storage.load_tasks()
        assert loaded == test_tasks, "Save/load should preserve data"
        
        # Test next_id
        assert storage.get_next_id([]) == 1, "First ID should be 1"
        assert storage.get_next_id([{"id": 5}]) == 6, "Next ID should increment"
    
    print("  ✓ Storage tests passed")


def test_task_manager():
    """Test TaskManager operations."""
    print("Testing TaskManager...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "tasks.json")
        storage = TaskStorage(data_file)
        manager = TaskManager(storage)
        
        # Test add
        task = manager.add_task("Test task", "high", "Description")
        assert task["id"] == 1
        assert task["title"] == "Test task"
        assert task["priority"] == "high"
        assert task["completed"] == False
        
        # Test get
        retrieved = manager.get_task(1)
        assert retrieved == task
        assert manager.get_task(999) is None
        
        # Test list
        manager.add_task("Low priority", "low")
        manager.add_task("Medium task", "medium")
        all_tasks = manager.list_tasks()
        assert len(all_tasks) == 3
        
        # Test filter by priority
        high_tasks = manager.list_tasks(priority="high")
        assert len(high_tasks) == 1
        assert high_tasks[0]["priority"] == "high"
        
        # Test complete
        manager.complete_task(1)
        task = manager.get_task(1)
        assert task["completed"] == True
        assert task["completed_at"] is not None
        
        # Test filter by status
        completed = manager.list_tasks(status="completed")
        assert len(completed) == 1
        pending = manager.list_tasks(status="pending")
        assert len(pending) == 2
        
        # Test uncomplete
        manager.uncomplete_task(1)
        assert manager.get_task(1)["completed"] == False
        
        # Test update
        manager.update_task(1, title="Updated", priority="low")
        task = manager.get_task(1)
        assert task["title"] == "Updated"
        assert task["priority"] == "low"
        
        # Test stats
        stats = manager.get_stats()
        assert stats["total"] == 3
        assert stats["pending"] == 3
        
        # Test delete
        assert manager.delete_task(1) == True
        assert manager.delete_task(999) == False
        assert len(manager.list_tasks()) == 2
        
        # Test clear completed
        manager.complete_task(2)
        cleared = manager.clear_completed()
        assert cleared == 1
        assert len(manager.list_tasks()) == 1
    
    print("  ✓ TaskManager tests passed")


def test_priority_validation():
    """Test priority validation."""
    print("Testing Priority Validation...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "tasks.json")
        storage = TaskStorage(data_file)
        manager = TaskManager(storage)
        
        # Invalid priority defaults to medium
        task = manager.add_task("Test", "invalid")
        assert task["priority"] == "medium"
        
        # Valid priorities work
        for p in ["high", "medium", "low"]:
            t = manager.add_task(f"{p} task", p)
            assert t["priority"] == p
    
    print("  ✓ Priority validation tests passed")


if __name__ == "__main__":
    print("=" * 50)
    print("🧪 Task Tracker Test Suite")
    print("=" * 50)
    
    try:
        test_storage()
        test_task_manager()
        test_priority_validation()
        print("=" * 50)
        print("✅ All tests passed!")
        print("=" * 50)
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"💥 Error: {e}")
        sys.exit(1)
