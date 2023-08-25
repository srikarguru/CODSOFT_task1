from tkinter import Tk, Label, Entry, Button, Listbox, Scrollbar, END, messagebox

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List")

        # Task variables
        self.tasks = []

        # Create task labels
        title_label = Label(root, text="Add Items")
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.title_entry = Entry(root, width=30)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Create buttons
        create_button = Button(root, text="Create Task", command=self.create_task)
        create_button.grid(row=2, column=0, padx=10, pady=10)

        update_button = Button(root, text="Update Task", command=self.update_task)
        update_button.grid(row=2, column=1, padx=10, pady=10)

        delete_button = Button(root, text="Delete Task", command=self.delete_task)
        delete_button.grid(row=2, column=2, padx=10, pady=10)

        # Create task listbox
        self.task_listbox = Listbox(root, width=70, height=10)
        self.task_listbox.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="w")

        scrollbar = Scrollbar(root)
        scrollbar.grid(row=3, column=3, sticky="ns")
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)

        # Load tasks from file
        self.load_tasks()

        # Bind double-click event on the listbox
        self.task_listbox.bind("<Double-Button-1>", self.mark_task_as_completed)

        # Lock the screen from expanding
        self.root.resizable(width=False, height=False)

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                self.tasks = file.read().splitlines()
        except FileNotFoundError:
            self.tasks = []

        self.update_task_listbox()

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                file.write(task + "\n")

    def create_task(self):
        title = self.title_entry.get()
        if title:
            task = f"{title}"
            self.tasks.append(task)
            self.update_task_listbox()
            self.clear_entry_fields()
            self.save_tasks()
            messagebox.showinfo("Task Created", "Task created successfully!")
        else:
            messagebox.showwarning("Empty Field", "Please enter a task title.")

    def update_task(self):
        selected_task = self.task_listbox.curselection()

        if selected_task:
            title = self.title_entry.get()

            if title:
                task = f"{title}"
                self.tasks[selected_task[0]] = task
                self.update_task_listbox()
                self.clear_entry_fields()
                self.save_tasks()
                messagebox.showinfo("Task Updated", "Task updated successfully!")
            else:
                messagebox.showwarning("Empty Field", "Please enter a task title.")
        else:
            messagebox.showwarning("No Task Selected", "Please select a task to update.")

    def delete_task(self):
        selected_task = self.task_listbox.curselection()

        if selected_task:
            self.tasks.pop(selected_task[0])
            self.update_task_listbox()
            self.save_tasks()
            messagebox.showinfo("Task Deleted", "Task deleted successfully!")
        else:
            messagebox.showwarning("No Task Selected", "Please select a task to delete.")

    def mark_task_as_completed(self, event):
        selected_task = self.task_listbox.curselection()

        if selected_task:
            task = self.tasks[selected_task[0]]
            if task.endswith(" (Completed)"):
                self.tasks[selected_task[0]] = task.replace(" (Completed)", "")
            else:
                self.tasks[selected_task[0]] = task + " (Completed)"
            self.update_task_listbox()
            self.save_tasks()

    def update_task_listbox(self):
        self.task_listbox.delete(0, END)
        for task in self.tasks:
            self.task_listbox.insert(END, task)

    def clear_entry_fields(self):
        self.title_entry.delete(0, END)

# Create the main window
root = Tk()

# Create the TodoApp object
app = TodoApp(root)

# Run the application's main event loop
root.mainloop()
