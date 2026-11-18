import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date

# ---------- COLORS ----------
BG = "#F4F6FB"
WHITE = "#FFFFFF"
PURPLE = "#635BFF"
DARK = "#20213A"
GREY = "#8589A6"

# ---------- DATABASE ----------
# Creates the database file automatically
conn = sqlite3.connect("finora.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        expense_date TEXT NOT NULL
    )
""")

conn.commit()

# ---------- MAIN WINDOW ----------
root = tk.Tk()
root.title("Finora - Personal Expense Tracker")
root.geometry("1100x760")
root.minsize(900, 650)
root.configure(bg=BG)

# ---------- SIDEBAR ----------
sidebar = tk.Frame(root, bg=DARK, width=210)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(
    sidebar,
    text="◈ Finora",
    font=("Arial", 23, "bold"),
    bg=DARK,
    fg=WHITE
).pack(anchor="w", padx=22, pady=(30, 45))

for item in ["Dashboard", "Add Expense", "Transactions"]:
    tk.Label(
        sidebar,
        text="   " + item,
        font=("Arial", 12),
        bg=DARK,
        fg=WHITE,
        anchor="w",
        padx=12,
        pady=14
    ).pack(fill="x", padx=12, pady=4)

# ---------- MAIN CONTENT ----------
content = tk.Frame(root, bg=BG)
content.pack(
    side="left",
    fill="both",
    expand=True,
    padx=25,
    pady=20
)

tk.Label(
    content,
    text="Dashboard",
    font=("Arial", 25, "bold"),
    bg=BG,
    fg=DARK
).pack(anchor="w")

tk.Label(
    content,
    text="Track your spending, one expense at a time.",
    font=("Arial", 11),
    bg=BG,
    fg=GREY
).pack(anchor="w", pady=(4, 18))

# ---------- SUMMARY CARDS ----------
cards = tk.Frame(content, bg=BG)
cards.pack(fill="x", pady=(0, 18))

def make_card(title, initial_value):
    card = tk.Frame(
        cards,
        bg=WHITE,
        highlightbackground="#E5E7F0",
        highlightthickness=1
    )
    card.pack(side="left", fill="both", expand=True, padx=(0, 10))

    tk.Label(
        card,
        text=title,
        font=("Arial", 9, "bold"),
        bg=WHITE,
        fg=GREY
    ).pack(anchor="w", padx=12, pady=(14, 6))

    value_label = tk.Label(
        card,
        text=initial_value,
        font=("Arial", 19, "bold"),
        bg=WHITE,
        fg=PURPLE
    )
    value_label.pack(anchor="w", padx=12, pady=(0, 14))

    return value_label

total_label = make_card("TOTAL SPENT", "₹0.00")
count_label = make_card("TRANSACTIONS", "0")
category_label = make_card("TOP CATEGORY", "None")

# ---------- EXPENSE FORM ----------
form = tk.Frame(
    content,
    bg=WHITE,
    highlightbackground="#E5E7F0",
    highlightthickness=1
)
form.pack(fill="x", pady=(0, 18))

tk.Label(
    form,
    text="Add a New Expense",
    font=("Arial", 15, "bold"),
    bg=WHITE,
    fg=DARK
).pack(anchor="w", padx=15, pady=(12, 8))

tk.Label(
    form,
    text="Expense name",
    bg=WHITE,
    fg=DARK
).pack(anchor="w", padx=15)

expense_entry = tk.Entry(form, font=("Arial", 11))
expense_entry.pack(fill="x", padx=15, pady=(3, 8), ipady=4)

tk.Label(
    form,
    text="Amount (₹)",
    bg=WHITE,
    fg=DARK
).pack(anchor="w", padx=15)

amount_entry = tk.Entry(form, font=("Arial", 11))
amount_entry.pack(fill="x", padx=15, pady=(3, 8), ipady=4)

tk.Label(
    form,
    text="Category",
    bg=WHITE,
    fg=DARK
).pack(anchor="w", padx=15)

category_box = ttk.Combobox(
    form,
    values=[
        "Food", "Transport", "Shopping",
        "Education", "Bills", "Health", "Other"
    ],
    state="readonly",
    font=("Arial", 10)
)
category_box.pack(fill="x", padx=15, pady=(3, 10), ipady=3)
category_box.set("Food")

def add_expense():
    name = expense_entry.get().strip()
    amount_text = amount_entry.get().strip()
    category = category_box.get()

    if not name or not amount_text:
        messagebox.showwarning(
            "Missing Information",
            "Please enter the expense name and amount."
        )
        return

    try:
        amount = float(amount_text)

        if amount <= 0:
            messagebox.showwarning(
                "Invalid Amount",
                "Amount must be greater than zero."
            )
            return

    except ValueError:
        messagebox.showwarning(
            "Invalid Amount",
            "Enter a valid number, such as 120 or 99.50."
        )
        return

    cursor.execute(
        """INSERT INTO expenses
           (name, amount, category, expense_date)
           VALUES (?, ?, ?, ?)""",
        (name, amount, category, date.today().isoformat())
    )
    conn.commit()

    expense_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    category_box.set("Food")

    update_dashboard()

    messagebox.showinfo(
        "Finora",
        f"{name} saved successfully!\nAmount: ₹{amount:.2f}"
    )

tk.Button(
    form,
    text="＋  Add Expense",
    command=add_expense,
    font=("Arial", 10, "bold"),
    bg=PURPLE,
    fg=WHITE,
    activebackground="#5148E5",
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    padx=12,
    pady=7
).pack(anchor="w", padx=15, pady=(0, 12))

# ---------- TRANSACTION TABLE ----------
tk.Label(
    content,
    text="Recent Transactions",
    font=("Arial", 15, "bold"),
    bg=BG,
    fg=DARK
).pack(anchor="w", pady=(0, 8))

table_frame = tk.Frame(content, bg=WHITE)
table_frame.pack(fill="both", expand=True)

columns = ("name", "amount", "category", "date")

transaction_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=7
)

transaction_table.heading("name", text="Expense")
transaction_table.heading("amount", text="Amount (₹)")
transaction_table.heading("category", text="Category")
transaction_table.heading("date", text="Date")

transaction_table.column("name", width=180)
transaction_table.column("amount", width=110)
transaction_table.column("category", width=120)
transaction_table.column("date", width=110)

transaction_table.pack(
    side="left",
    fill="both",
    expand=True,
    padx=5,
    pady=5
)

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=transaction_table.yview
)
scrollbar.pack(side="right", fill="y")

transaction_table.configure(yscrollcommand=scrollbar.set)

# ---------- UPDATE DASHBOARD ----------
def update_dashboard():
    cursor.execute(
        "SELECT COALESCE(SUM(amount), 0), COUNT(*) FROM expenses"
    )
    total, count = cursor.fetchone()

    total_label.config(text=f"₹{total:,.2f}")
    count_label.config(text=str(count))

    cursor.execute("""
        SELECT category
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC, category ASC
        LIMIT 1
    """)
    result = cursor.fetchone()

    category_label.config(
        text=result[0] if result else "None"
    )

    for item in transaction_table.get_children():
        transaction_table.delete(item)

    cursor.execute("""
        SELECT name, amount, category, expense_date
        FROM expenses
        ORDER BY id DESC
    """)

    for name, amount, category, expense_date in cursor.fetchall():
        transaction_table.insert(
            "",
            tk.END,
            values=(name, f"{amount:,.2f}", category, expense_date)
        )

# Load saved expenses when the app starts
update_dashboard()

# ---------- CLOSE APPLICATION ----------
def close_app():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close_app)

# ---------- RUN APPLICATION ----------
root.mainloop()
