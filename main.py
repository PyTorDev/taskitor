import sys
from commands import (
    add_task,
    delete_task,
    update_task,
    change_status,
    list_tasks,
)

def main():
    if len(sys.argv) < 2:
        print("Please provide a command: add, delete, update, change_status, list")
        return
    
    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Usage: add \"description\"")
            return
        description = sys.argv[2]
        add_task(description)

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: delete <id>")
            return
        delete_task(int(sys.argv[2]))

    elif command == "update":
        if len(sys.argv) < 4:
            print("Usage: update <id> \"new description\"")
            return
        update_task(int(sys.argv[2]), sys.argv[3])

    elif command == "status":
        if len(sys.argv) < 4:
            print("Usage: status <id> <status>")
            return
        change_status(int(sys.argv[2]), sys.argv[3])

    elif command == "list":
        status = sys.argv[2] if len(sys.argv) >= 3 else None
        list_tasks(status)

    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()