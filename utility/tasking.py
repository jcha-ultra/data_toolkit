"""
Functionality for managing tasks.
"""

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Dict, List, Union

TaskJsonDict = Dict[str, Union[None, bool, str, List["TaskJsonDict"]]]


@dataclass
class Task:
    """A task to be completed by a user."""

    name: str
    """The name of the task."""

    description: str
    """The description of the task."""

    file: Union[str, None] = None
    """The file the task is serialized to."""

    completed: bool = False
    """Whether the task has been completed."""

    subtasks: Union["list[Task]", None] = None
    """The subtasks of the task."""

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> "Task":
        """Create a task from a JSON dictionary."""

        # validate json_dict keys
        missing_keys = set(cls.__dataclass_fields__.keys()) - set( # pylint: disable=no-member
            json_dict.keys()
        )
        if missing_keys:
            raise ValueError(f"JSON dictionary is missing keys: {missing_keys}")

        return cls(
            name=json_dict["name"],
            description=json_dict["description"],
            file=json_dict["file"],
            completed=json_dict["completed"],
            subtasks=[Task.from_json_dict(subtask) for subtask in json_dict["subtasks"]]
            if json_dict["subtasks"]
            else None,
        )

    @classmethod
    def from_file(cls, path: Union[str, Path]) -> "Task":
        """Create a task from a file."""
        with open(path, "r", encoding="utf-8") as file:
            return cls.from_json_dict(json.loads(file.read()))

    def to_json_dict(self) -> TaskJsonDict:
        """Get the JSON representation of the task."""
        return {
            "name": self.name,
            "description": self.description,
            "file": self.file,
            "completed": self.completed,
            "subtasks": [subtask.to_json_dict() for subtask in self.subtasks]
            if self.subtasks
            else None,
        }

    def __str__(self) -> str:
        """Get the string representation of the task."""
        return f"{self.name}: {self.description}"

    def __repr__(self) -> str:
        """Get the string representation of the task, which is a JSON that can be used to reconstruct the task."""
        return json.dumps(self.to_json_dict(), indent=4)

    def __eq__(self, other: "Task") -> bool:
        """Compare two tasks for equality."""
        return self.to_json_dict() == other.to_json_dict()

    def write_to_file(self, root_dir: str) -> None:
        """Write the task to a file."""
        if self.file is None:
            raise ValueError("Task has no file to write to.")
        with open(Path(root_dir, self.file), "w", encoding="utf-8") as file:
            file.write(repr(self))

    def add_subtask(self, subtask: "Task") -> None:
        """Add a subtask to the task."""
        if self.subtasks is None:
            self.subtasks = []
        self.subtasks.append(subtask)


def test(test_dir: str) -> None:
    """Test the tasking module."""
    task = Task(
        name="Test Task",
        description="This is a test task.",
        file="test_task.json",
        completed=False,
        subtasks=[
            Task(
                name="Subtask 1",
                description="This is a subtask.",
                file="subtask_1.json",
                completed=False,
            ),
            Task(
                name="Subtask 2",
                description="This is another subtask.",
                file="subtask_2.json",
                completed=False,
            ),
        ],
    )
    task.write_to_file(test_dir)
    task_from_file = Task.from_file(Path(test_dir, task.file))  # type: ignore
    assert task == task_from_file


if __name__ == "__main__":
    test("test_data/tasking")
