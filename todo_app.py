import sqlite3
from datetime import datetime

DB_NAME = "todo.db"

def create_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status INTEGER DEFAULT 0,  -- 0: pending, 1: completed
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_task(task_description):
    conn = create_connection()
    cursor = conn.cursor()
    created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO tasks (task, created_at) VALUES (?, ?)", (task_description, created))
    conn.commit()
    conn.close()
    print("Task added!")

def view_tasks():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, status, created_at FROM tasks ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        print("No tasks yet!")
        return
    
    print("\nYour To-Do List:")
    print("-" * 50)
    for row in rows:
        task_id, task, status, created = row
        status_str = "Done" if status == 1 else "Pending"
        print(f"{task_id}. [{status_str}] {task}  (Added: {created})")
    print("-" * 50)

def complete_task(task_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 1 WHERE id = ?", (task_id,))
    if cursor.rowcount == 0:
        print("Task ID not found!")
    else:
        print("Task marked as completed!")
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    if cursor.rowcount == 0:
        print("Task ID not found!")
    else:
        print("Task deleted!")
    conn.commit()
    conn.close()

def main_menu():
    create_table()  # Ensure table exists
    while True:
        print("\n=== To-Do List Manager ===")
        print("1. Add new task")
        print("2. View all tasks")
        print("3. Mark task as completed")
        print("4. Delete task")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == "1":
            task = input("Enter task description: ").strip()
            if task:
                add_task(task)
            else:
                print("Task cannot be empty!")
        
        elif choice == "2":
            view_tasks()
        
        elif choice == "3":
            view_tasks()
            try:
                task_id = int(input("Enter task ID to mark completed: "))
                complete_task(task_id)
            except ValueError:
                print("Please enter a valid number!")
        
        elif choice == "4":
            view_tasks()
            try:
                task_id = int(input("Enter task ID to delete: "))
                delete_task(task_id)
            except ValueError:
                print("Please enter a valid number!")
        
        elif choice == "5":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main_menu()