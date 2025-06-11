# Project: Taskitor CLI – Task Tracker

## Overview

Taskitor is a command-line application written in Python that allows users to manage their tasks through simple CLI commands. Tasks are stored in a local JSON file and can have three possible statuses: "to-do", "in-progress", and "done".

The goal is to enhance the visual appearance of the CLI output using the `rich` library, making the interface more readable and user-friendly.

## Agent Objective

The AI agent should assist with:
- Enhancing CLI output using the `rich` library (tables, colors, formatted messages)
- Keeping the code clean, readable, and well-documented
- Avoiding changes to existing functionality or business logic
- Not adding any dependencies beyond `rich`

## Project Structure

- `main.py`: Entry point that parses CLI arguments and dispatches commands
- `task.py`: Defines the `Task` class and valid status constants
- `storage.py`: Functions for reading/writing tasks to `tasks.json`
- `commands.py`: Logic for task operations (`add`, `delete`, `update`, `change_status`, `list_tasks`)
- `tests/`: Contains unit tests using the `unittest` module
- `tasks.json`: JSON file where task data is stored (created automatically)

## Desired Output

Output formatting should:
- Show error messages in red
- Show success/confirmation messages in green or cyan
- Display task lists as tables with headers (ID, description, status, timestamps)
- Optionally include subtle symbols or emojis for visual clarity

## Constraints

- Do not rename or alter the existing command interface
- Do not change the structure or content of the JSON data
- Do not introduce any graphical or web-based interfaces
- Must maintain compatibility with Python 3.10+

## Allowed Libraries

- ✅ `rich` is allowed and preferred for all output formatting
- ❌ No other third-party libraries or frameworks should be added

## Priorities

1. Visually clear and polished terminal output
2. Maintain clean, maintainable code
3. Do not break or alter core functionality
