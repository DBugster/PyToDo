import tkinter as tk
from tkinter import messagebox
from taskDB import TaskDB  # <-- Add this import

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDo List Manager")
        self.root.geometry("400x350")
        self.root.configure(bg="#f0f4f8")

        self.db = TaskDB()  # <-- Use the TaskDB class
        self.tasks = []

        self.frame = tk.Frame(root, bg="#f0f4f8")
        self.frame.pack(padx=10, pady=15)

        self.task_entry = tk.Entry(self.frame, width=28, font=("Segoe UI", 12), bd=2, relief=tk.GROOVE)
        self.task_entry.pack(side=tk.LEFT, padx=(0, 8), ipady=4)
        self.task_entry.bind('<Return>', lambda event: self.add_task())

        self.add_btn = tk.Button(
            self.frame, text="Add Task", command=self.add_task,
            bg="#4caf50", fg="white", font=("Segoe UI", 10, "bold"),
            activebackground="#388e3c", activeforeground="white", bd=0, padx=10, pady=4
        )
        self.add_btn.pack(side=tk.LEFT)

        self.listbox_frame = tk.Frame(root, bg="#f0f4f8")
        self.listbox_frame.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(
            self.listbox_frame, width=45, height=12, selectmode=tk.SINGLE,
            font=("Segoe UI", 11), bd=2, relief=tk.GROOVE, bg="#ffffff", fg="#333333",
            selectbackground="#90caf9", selectforeground="#0d47a1"
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.button_frame = tk.Frame(root, bg="#f0f4f8")
        self.button_frame.pack(pady=(0, 10))

        self.done_btn = tk.Button(
            self.button_frame, text="Mark as Done", command=self.mark_done,
            bg="#1976d2", fg="white", font=("Segoe UI", 10, "bold"),
            activebackground="#1565c0", activeforeground="white", bd=0, padx=12, pady=4
        )
        self.done_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.delete_btn = tk.Button(
            self.button_frame, text="Delete Task", command=self.delete_task,
            bg="#e53935", fg="white", font=("Segoe UI", 10, "bold"),
            activebackground="#b71c1c", activeforeground="white", bd=0, padx=12, pady=4
        )
        self.delete_btn.pack(side=tk.LEFT)

        self.load_tasks()  # <-- Load tasks from DB at startup

    def load_tasks(self):
        self.tasks = []
        self.listbox.delete(0, tk.END)
        for task, done in self.db.get_tasks():
            display_task = f"[Done] {task}" if done else task
            self.tasks.append(display_task)
            self.listbox.insert(tk.END, display_task)

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.db.add_task(task)
            self.load_tasks()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a task.")

    def delete_task(self):
        selected = self.listbox.curselection()
        if selected:
            idx = selected[0]
            task_text = self.tasks[idx].replace("[Done] ", "")
            self.db.delete_task(task_text)
            self.load_tasks()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def mark_done(self):
        selected = self.listbox.curselection()
        if selected:
            idx = selected[0]
            task_text = self.tasks[idx].replace("[Done] ", "")
            self.db.mark_done(task_text)
            self.load_tasks()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as done.")

    def __del__(self):
        self.db.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()