import tkinter as tk
from tkinter import messagebox, ttk
from collections import defaultdict

class Income:
    def __init__(self, name, amount, frequency):
        self.name = name
        self.amount = amount
        self.frequency = frequency

    def display(self):
        return f"Income: {self.name}, Amount: ${self.amount}, Frequency: {self.frequency}"

class Expense:
    def __init__(self, name, amount, category):
        self.name = name
        self.amount = amount
        self.category = category

    def display(self):
        return f"Expense: {self.name}, Amount: ${self.amount}, Category: {self.category}"

class BudgetingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Budgeting App")
        self.geometry("1000x600")
        self.configure(background='lightgrey')

        self.income_sources = []
        self.expenses = []

        # Center the window
        self.center_window()

        # Create a frame for input fields
        self.input_frame = tk.Frame(self, bg='lightgrey')
        self.input_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')

        # Create a frame for budget summary
        self.summary_frame = tk.Frame(self, bg='lightgrey')
        self.summary_frame.grid(row=0, column=1, padx=20, pady=20, sticky='nsew')

        # Labels and entries for user inputs
        self.income_label = tk.Label(self.input_frame, text="Income Source:", bg='lightgrey', font=("Arial", 12))
        self.income_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.income_entry = tk.Entry(self.input_frame)
        self.income_entry.grid(row=0, column=1, padx=10, pady=5)

        self.amount_label = tk.Label(self.input_frame, text="Amount ($):", bg='lightgrey', font=("Arial", 12))
        self.amount_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.amount_entry = tk.Entry(self.input_frame)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=5)

        self.frequency_label = tk.Label(self.input_frame, text="Frequency:", bg='lightgrey', font=("Arial", 12))
        self.frequency_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.frequency_entry = tk.Entry(self.input_frame)
        self.frequency_entry.grid(row=2, column=1, padx=10, pady=5)

        self.category_label = tk.Label(self.input_frame, text="Expense Category:", bg='lightgrey', font=("Arial", 12))
        self.category_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')
        self.category_entry = tk.Entry(self.input_frame)
        self.category_entry.grid(row=3, column=1, padx=10, pady=5)

        self.expense_label = tk.Label(self.input_frame, text="Expense ($):", bg='lightgrey', font=("Arial", 12))
        self.expense_label.grid(row=4, column=0, padx=10, pady=5, sticky='w')
        self.expense_entry = tk.Entry(self.input_frame)
        self.expense_entry.grid(row=4, column=1, padx=10, pady=5)

        # Button to add income source
        self.add_income_button = tk.Button(self.input_frame, text="Add Income", command=self.add_income, bg='lightgreen', font=("Arial", 12))
        self.add_income_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky='we')

        # Button to add expense
        self.add_expense_button = tk.Button(self.input_frame, text="Add Expense", command=self.add_expense, bg='lightgreen', font=("Arial", 12))
        self.add_expense_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky='we')

        # Budget summary label
        self.summary_label = tk.Label(self.summary_frame, text="Budget Summary", bg='lightgrey', font=("Arial", 14, 'bold'))
        self.summary_label.pack(pady=(0,10))

        # Table to display data
        self.tree = ttk.Treeview(self.summary_frame, columns=('Description', 'Amount'), show='headings')
        self.tree.heading('Description', text='Description')
        self.tree.heading('Amount', text='Amount ($)')
        self.tree.pack(fill='both', expand=True)

        # Pie chart canvas
        self.pie_canvas = tk.Canvas(self.summary_frame, bg='white', width=400, height=300)  # Set width and height for canvas
        self.pie_canvas.pack(pady=(10, 0), fill='both', expand=True)

        # Legend for pie chart
        self.legend_frame = tk.Frame(self.summary_frame, bg='lightgrey')
        self.legend_frame.pack(pady=(10,0))

        # Table to label pie chart colors
        self.color_label_table = ttk.Treeview(self.summary_frame, columns=('Color', 'Category'), show='headings')
        self.color_label_table.heading('Color', text='Color')
        self.color_label_table.heading('Category', text='Category')
        self.color_label_table.pack(pady=(10, 0), fill='both', expand=True)

        # Draw initial pie chart, legend, and color label table
        self.draw_pie_chart()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 1000
        window_height = 600
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def add_income(self):
        name = self.income_entry.get()
        amount = self.amount_entry.get()
        frequency = self.frequency_entry.get()

        if name and amount and frequency:
            try:
                amount = float(amount)  # Convert amount to float
                income = Income(name, amount, frequency)
                self.income_sources.append(income)
                self.update_budget_summary()
            except ValueError:
                messagebox.showwarning("Warning", "Amount must be a number.")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields for income.")

    def add_expense(self):
        name = self.expense_entry.get()
        amount = self.expense_entry.get()
        category = self.category_entry.get()

        if name and amount and category:
            try:
                amount = float(amount)  # Convert amount to float
                expense = Expense(name, amount, category)
                self.expenses.append(expense)
                self.update_budget_summary()
            except ValueError:
                messagebox.showwarning("Warning", "Amount must be a number.")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields for expense.")

    def update_budget_summary(self):
        # Clear treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Display income sources
        for income in self.income_sources:
            self.tree.insert('', 'end', values=(income.display(), f"${income.amount}"))

        # Display expenses
        for expense in self.expenses:
            self.tree.insert('', 'end', values=(expense.display(), f"${expense.amount}"))

        # Update pie chart
        self.draw_pie_chart()

    def draw_pie_chart(self):
        categories = defaultdict(float)
        for expense in self.expenses:
            categories[expense.category] += expense.amount

        total = sum(categories.values())
        start_angle = 0
        self.pie_canvas.delete("all")  # Clear previous drawings
        self.legend_frame.destroy()  # Clear previous legend
        self.color_label_table.delete(*self.color_label_table.get_children())  # Clear previous color labels

        legend_labels = []
        color_mapping = {
            0: 'red',
            1: 'blue',
            2: 'green',
            3: 'orange',
            4: 'purple',
            5: 'pink',
            6: 'yellow',
            7: 'cyan',
            8: 'brown',
            9: 'black'
        }

        for i, (category, amount) in enumerate(categories.items()):
            proportion = amount / total
            extent_angle = 360 * proportion
            # Ensure the pie chart fits within the canvas
            self.pie_canvas.create_arc(10, 10, 290, 290, start=start_angle, extent=extent_angle, fill=color_mapping[i % len(color_mapping)], style='pieslice')

            # Add legend label
            legend_labels.append(f"{category}: ${amount:.2f}")

            # Add color label to the table
            self.color_label_table.insert('', 'end', values=(color_mapping[i % len(color_mapping)], category))

            start_angle += extent_angle

        # Create legend
        for i, label in enumerate(legend_labels):
            tk.Label(self.legend_frame, text=label, bg='lightgrey').grid(row=i, column=0, sticky='w')

    def get_random_color(self):
        import random
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

if __name__ == "__main__":
    app = BudgetingApp()
    app.mainloop()
