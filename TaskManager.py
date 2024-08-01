import tkinter as tk
from tkinter import messagebox, simpledialog, MULTIPLE
import json

class Task:
    def __init__(self, description, completed=False):
        self.description = description
        self.completed = completed

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def complete_task(self, task):
        task.completed = not task.completed

    def to_dict(self):
        return {"tasks": [{"description": task.description, "completed": task.completed} for task in self.tasks]}

    def from_dict(self, data):
        self.tasks = [Task(task_data["description"], task_data["completed"]) for task_data in data["tasks"]]

class TaskApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Task Manager")

        self.task_manager = TaskManager()

        self.task_entry = tk.Entry(master, width=30, font=('Helvetica', 14))
        self.task_entry.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.add_button = tk.Button(
            master, text="Add Task", command=self.add_task, font=('Helvetica', 12), bg='#4CAF50', fg='white')
        self.add_button.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        self.task_frame = tk.Frame(master)
        self.task_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.complete_button = tk.Button(
            self.task_frame, text="Complete Task(s)", command=self.complete_task, font=('Helvetica', 12), bg='#2196F3', fg='white')
        self.complete_button.grid(row=0, column=0, padx=5)

        self.remove_button = tk.Button(
            self.task_frame, text="Remove Task(s)", command=self.remove_task, font=('Helvetica', 12), bg='#F44336', fg='white')
        self.remove_button.grid(row=0, column=1, padx=5)

        self.task_list_frame = tk.Frame(master)
        self.task_list_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.task_listbox = tk.Listbox(self.task_list_frame, width=40, height=10, font=('Helvetica', 12), selectbackground="#a6a6a6", selectmode=MULTIPLE)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.task_list_frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox.config(yscrollcommand=self.scrollbar.set)

        self.save_button = tk.Button(
            master, text="Save", command=self.save_tasks, font=('Helvetica', 12), bg='#FFC107', fg='black')
        self.save_button.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

        self.load_tasks()  # Load tasks from file when the app starts
        self.update_task_listbox()

    def add_task(self):
        try:
            task_description = self.task_entry.get().strip()
            if task_description:
                new_task = Task(task_description)
                self.task_manager.add_task(new_task)
                self.update_task_listbox()
                self.task_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while adding a task: {str(e)}")

    def complete_task(self):
        try:
            selected_indices = self.task_listbox.curselection()
            for index in selected_indices:
                selected_task = self.task_manager.tasks[index]
                self.task_manager.complete_task(selected_task)
            self.update_task_listbox()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while completing tasks: {str(e)}")

    def remove_task(self):
        try:
            selected_indices = self.task_listbox.curselection()
            for index in sorted(selected_indices, reverse=True):
                selected_task = self.task_manager.tasks[index]
                self.task_manager.remove_task(selected_task)
            self.update_task_listbox()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while removing tasks: {str(e)}")

    def update_task_listbox(self):
        try:
            self.task_listbox.delete(0, tk.END)
            for task in self.task_manager.tasks:
                status = "✓" if task.completed else "◻"
                self.task_listbox.insert(tk.END, f"  {status} {task.description}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while updating the task list: {str(e)}")

    def save_tasks(self):
        try:
            with open("tasks.json", "w") as file:
                json.dump(self.task_manager.to_dict(), file)
            messagebox.showinfo("Save Successful", "Tasks have been successfully saved!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving tasks: {str(e)}")

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                data = json.load(file)
                self.task_manager.from_dict(data)
        except FileNotFoundError:
            pass  # If the file doesn't exist, there are no tasks to load
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading tasks: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x500")  # Set a fixed size for the window
    root.resizable(False, False)  # Disable window resizing
    task_app = TaskApp(root)
    root.mainloop()
