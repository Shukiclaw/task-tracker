#!/usr/bin/env python3
"""Task Tracker CLI - Main entry point."""
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

from task_manager import TaskManager
from storage import TaskStorage


console = Console()


def get_manager():
    """Get TaskManager instance."""
    return TaskManager()


def priority_color(priority: str) -> str:
    """Get color for priority level."""
    return {
        "high": "red",
        "medium": "yellow",
        "low": "green",
    }.get(priority, "white")


def status_symbol(completed: bool) -> str:
    """Get status symbol."""
    return "✅" if completed else "⏳"


@click.group()
@click.version_option(version="1.0.0", prog_name="task-tracker")
def cli():
    """📝 Task Tracker - Command-line task management made simple."""
    pass


@cli.command()
@click.argument("title")
@click.option("--priority", "-p", default="medium", 
              type=click.Choice(["high", "medium", "low"], case_sensitive=False),
              help="Task priority level")
@click.option("--description", "-d", default="", help="Optional task description")
def add(title, priority, description):
    """Add a new task."""
    manager = get_manager()
    task = manager.add_task(title, priority, description)
    
    console.print(Panel(
        f"[bold green]Task added successfully![/bold green]\n\n"
        f"ID: {task['id']}\n"
        f"Title: {task['title']}\n"
        f"Priority: [{priority_color(priority)}]{priority.upper()}[/{priority_color(priority)}]",
        title="📝 New Task",
        border_style="green"
    ))


@cli.command()
@click.option("--status", "-s", 
              type=click.Choice(["completed", "pending", "all"]),
              default="all", help="Filter by status")
@click.option("--priority", "-p",
              type=click.Choice(["high", "medium", "low"]),
              help="Filter by priority")
def list(status, priority):
    """List all tasks with optional filtering."""
    manager = get_manager()
    
    # Map 'all' to None for no filtering
    status_filter = status if status != "all" else None
    tasks = manager.list_tasks(status=status_filter, priority=priority)
    
    if not tasks:
        console.print("[dim]No tasks found.[/dim]")
        return
    
    table = Table(
        title="📝 Your Tasks",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )
    
    table.add_column("ID", style="dim", width=4)
    table.add_column("Status", width=6, justify="center")
    table.add_column("Priority", width=10)
    table.add_column("Title", min_width=20)
    table.add_column("Description", style="dim", max_width=30)
    
    for task in tasks:
        status_emoji = status_symbol(task.get("completed", False))
        priority = task.get("priority", "medium")
        title_text = task.get("title", "")
        
        # Strikethrough for completed tasks
        if task.get("completed"):
            title_text = f"[strike]{title_text}[/strike]"
        
        table.add_row(
            str(task["id"]),
            status_emoji,
            f"[{priority_color(priority)}]{priority.upper()}[/{priority_color(priority)}]",
            title_text,
            task.get("description", "")[:50]
        )
    
    console.print(table)
    console.print(f"\n[dim]Showing {len(tasks)} task(s)[/dim]")


@cli.command()
@click.argument("task_id", type=int)
def complete(task_id):
    """Mark a task as completed."""
    manager = get_manager()
    task = manager.complete_task(task_id)
    
    if task:
        console.print(f"[green]✅ Task #{task_id} marked as completed![/green]")
    else:
        console.print(f"[red]❌ Task #{task_id} not found.[/red]")


@cli.command()
@click.argument("task_id", type=int)
def uncomplete(task_id):
    """Reopen a completed task."""
    manager = get_manager()
    task = manager.uncomplete_task(task_id)
    
    if task:
        console.print(f"[yellow]⏳ Task #{task_id} reopened![/yellow]")
    else:
        console.print(f"[red]❌ Task #{task_id} not found.[/red]")


@cli.command()
@click.argument("task_id", type=int)
@click.confirmation_option(prompt="Are you sure you want to delete this task?")
def delete(task_id):
    """Delete a task permanently."""
    manager = get_manager()
    if manager.delete_task(task_id):
        console.print(f"[green]🗑️  Task #{task_id} deleted.[/green]")
    else:
        console.print(f"[red]❌ Task #{task_id} not found.[/red]")


@cli.command()
@click.argument("task_id", type=int)
@click.option("--title", "-t", help="New title")
@click.option("--description", "-d", help="New description")
@click.option("--priority", "-p", 
              type=click.Choice(["high", "medium", "low"]),
              help="New priority")
def update(task_id, title, description, priority):
    """Update a task's details."""
    manager = get_manager()
    task = manager.update_task(task_id, title, description, priority)
    
    if task:
        console.print(f"[green]✏️  Task #{task_id} updated![/green]")
    else:
        console.print(f"[red]❌ Task #{task_id} not found.[/red]")


@cli.command()
def stats():
    """Show task statistics."""
    manager = get_manager()
    stats = manager.get_stats()
    
    # Create stats display
    total_text = Text()
    total_text.append(f"Total Tasks: ", style="bold")
    total_text.append(str(stats["total"]), style="cyan")
    
    completed_text = Text()
    completed_text.append(f"Completed: ", style="bold")
    completed_text.append(str(stats["completed"]), style="green")
    
    pending_text = Text()
    pending_text.append(f"Pending: ", style="bold")
    pending_text.append(str(stats["pending"]), style="yellow")
    
    console.print(Panel(
        f"[bold cyan]📊 Task Statistics[/bold cyan]\n\n"
        f"Total Tasks: [bold]{stats['total']}[/bold]\n"
        f"✅ Completed: [green]{stats['completed']}[/green]\n"
        f"⏳ Pending: [yellow]{stats['pending']}[/yellow]\n\n"
        f"[dim]Pending by Priority:[/dim]\n"
        f"  🔴 High: {stats['high_priority']}\n"
        f"  🟡 Medium: {stats['medium_priority']}\n"
        f"  🟢 Low: {stats['low_priority']}",
        border_style="cyan"
    ))


@cli.command(name="clear-completed")
@click.confirmation_option(prompt="Delete all completed tasks?")
def clear_completed():
    """Remove all completed tasks."""
    manager = get_manager()
    count = manager.clear_completed()
    console.print(f"[green]🧹 Cleared {count} completed task(s).[/green]")


@cli.command()
def interactive():
    """Launch interactive mode (shows help)."""
    console.print(Panel(
        "[bold cyan]Task Tracker CLI[/bold cyan]\n\n"
        "Quick commands:\n"
        "  [green]tt add \"Task name\" -p high[/green]     Add high priority task\n"
        "  [green]tt list[/green]                      Show all tasks\n"
        "  [green]tt list -s pending -p high[/green]   Show pending high priority\n"
        "  [green]tt complete 1[/green]                Mark task #1 done\n"
        "  [green]tt delete 1[/green]                  Delete task #1\n"
        "  [green]tt stats[/green]                     Show statistics\n\n"
        "Use [bold]tt --help[/bold] for all commands.",
        title="🚀 Interactive Mode",
        border_style="green"
    ))


if __name__ == "__main__":
    cli()
