
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
from datetime import date

# ---------- COLORS ----------
BG = "#F4F6FB"
WHITE = "#FFFFFF"
PURPLE = "#635BFF"
DARK = "#20213A"
GREY = "#8589A6"
RED = "#E34D59"
BORDER = "#E5E7F0"

CATEGORIES = [
    "Food", "Transport", "Shopping",
    "Education", "Bills", "Health", "Other"
]

# ---------- DATABASE ----------
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
root.geometry("1250x850")
root.minsize(1000, 700)
root.configure(bg=BG)

# ---------- STYLES ----------
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    foreground=DARK,
    rowheight=30,
    fieldbackground=WHITE,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    background="#E9EAF5",
    foreground=DARK,
    font=("Arial", 10, "bold"),
    padding=8
)

style.map(
    "Treeview",
    background=[("selected", PURPLE)],
    foreground=[("selected", WHITE)]
)

style.configure(
    "TCombobox",
    padding=5,
    font=("Arial", 10)
)

# ---------- SIDEBAR ----------
sidebar = tk.Frame(root, bg=DARK, width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(
    sidebar,
    text="◈ Finora",
    font=("Arial", 24, "bold"),
    bg=DARK,
    fg=WHITE
).pack(anchor="w", padx=22, pady=(28, 40))

def sidebar_button(text, action):
    tk.Button(
        sidebar,
        text=text,
        command=action,
        font=("Arial", 12),
        bg=DARK,
        fg=WHITE,
        activebackground=PURPLE,
        activeforeground=WHITE,
        relief="flat",
        anchor="w",
        padx=22,
        pady=13,
        cursor="hand2"
    ).pack(fill="x", padx=10, pady=3)

# ---------- MAIN CONTENT ----------
content = tk.Frame(root, bg=BG)
content.pack(
    side="left",
    fill="both",
    expand=True,
    padx=25,
    pady=18
)

# ---------- HEADER ----------
tk.Label(
    content,
    text="Dashboard",
    font=("Arial", 26, "bold"),
    bg=BG,
    fg=DARK
).pack(anchor="w")

tk.Label(
    content,
    text="Track your spending, one expense at a time.",
    font=("Arial", 11),
    bg=BG,
    fg=GREY
).pack(anchor="w", pady=(4, 14))

# ---------- SUMMARY CARDS ----------
cards = tk.Frame(content, bg=BG)
cards.pack(fill="x", pady=(0, 14))

def make_card(title, initial_value):
    card = tk.Frame(
        cards,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 10)
    )

    tk.Label(
        card,
        text=title,
        font=("Arial", 9, "bold"),
        bg=WHITE,
        fg=GREY
    ).pack(anchor="w", padx=14, pady=(12, 4))

    value_label = tk.Label(
        card,
        text=initial_value,
        font=("Arial", 19, "bold"),
        bg=WHITE,
        fg=PURPLE
    )
    value_label.pack(anchor="w", padx=14, pady=(0, 12))

    return value_label

total_label = make_card("TOTAL SPENT", "₹0.00")
count_label = make_card("TRANSACTIONS", "0")
category_label = make_card("TOP CATEGORY", "None")

# ---------- ADD EXPENSE FORM ----------
form = tk.Frame(
    content,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1
)
form.pack(fill="x", pady=(0, 12))

tk.Label(
    form,
    text="Add a New Expense",
    font=("Arial", 15, "bold"),
    bg=WHITE,
    fg=DARK
).pack(anchor="w", padx=15, pady=(10, 7))

fields = tk.Frame(form, bg=WHITE)
fields.pack(fill="x", padx=15)

# Expense name
name_frame = tk.Frame(fields, bg=WHITE)
name_frame.pack(side="left", fill="x", expand=True, padx=(0, 12))

tk.Label(
    name_frame,
    text="Expense name",
    bg=WHITE,
    fg=DARK
).pack(anchor="w")

expense_entry = tk.Entry(
    name_frame,
    font=("Arial", 11),
    relief="solid",
    bd=1
)
expense_entry.pack(fill="x", ipady=5, pady=(3, 8))

# Amount
amount_frame = tk.Frame(fields, bg=WHITE)
amount_frame.pack(side="left", fill="x", expand=True, padx=(0, 12))

tk.Label(
    amount_frame,
    text="Amount (₹)",
    bg=WHITE,
    fg=DARK
).pack(anchor="w")

amount_entry = tk.Entry(
    amount_frame,
    font=("Arial", 11),
    relief="solid",
    bd=1
)
amount_entry.pack(fill="x", ipady=5, pady=(3, 8))

# Category
category_frame = tk.Frame(fields, bg=WHITE)
category_frame.pack(side="left", fill="x", expand=True)

tk.Label(
    category_frame,
    text="Category",
    bg=WHITE,
    fg=DARK
).pack(anchor="w")

category_box = ttk.Combobox(
    category_frame,
    values=CATEGORIES,
    state="readonly",
    font=("Arial", 10)
)
category_box.pack(fill="x", ipady=3, pady=(3, 8))
category_box.set("Food")

# ---------- SEARCH VARIABLES ----------
search_var = tk.StringVar()
filter_var = tk.StringVar(value="All Categories")

# ---------- TRANSACTION TABLE ----------
table_title = tk.Label(
    content,
    text="Recent Transactions",
    font=("Arial", 15, "bold"),
    bg=BG,
    fg=DARK
)
table_title.pack(anchor="w", pady=(0, 8))

# Search and filter row
filter_frame = tk.Frame(content, bg=BG)
filter_frame.pack(fill="x", pady=(0, 8))

search_entry = tk.Entry(
    filter_frame,
    textvariable=search_var,
    font=("Arial", 10),
    width=22,
    relief="solid",
    bd=1
)
search_entry.pack(side="left", ipady=5, padx=(0, 8))

filter_box = ttk.Combobox(
    filter_frame,
    textvariable=filter_var,
    values=["All Categories"] + CATEGORIES,
    state="readonly",
    width=17
)
filter_box.pack(side="left", padx=(0, 8), ipady=3)

# Table container gets the remaining available height
table_frame = tk.Frame(content, bg=WHITE)
table_frame.pack(fill="both", expand=True)

columns = ("name", "amount", "category", "date")

transaction_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    selectmode="extended"
)

transaction_table.heading("name", text="Expense")
transaction_table.heading("amount", text="Amount (₹)")
transaction_table.heading("category", text="Category")
transaction_table.heading("date", text="Date")

transaction_table.column("name", width=220, minwidth=120, anchor="w")
transaction_table.column("amount", width=130, minwidth=100, anchor="center")
transaction_table.column("category", width=160, minwidth=100, anchor="center")
transaction_table.column("date", width=140, minwidth=110, anchor="center")

vertical_scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=transaction_table.yview
)

horizontal_scrollbar = ttk.Scrollbar(
    table_frame,
    orient="horizontal",
    command=transaction_table.xview
)

transaction_table.configure(
    yscrollcommand=vertical_scrollbar.set,
    xscrollcommand=horizontal_scrollbar.set
)

transaction_table.grid(row=0, column=0, sticky="nsew")
vertical_scrollbar.grid(row=0, column=1, sticky="ns")
horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

table_frame.rowconfigure(0, weight=1)
table_frame.columnconfigure(0, weight=1)

# ---------- DASHBOARD UPDATE ----------
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

    load_transactions()

# ---------- LOAD TRANSACTIONS ----------
def load_transactions():
    for item in transaction_table.get_children():
        transaction_table.delete(item)

    search_text = search_var.get().strip()
    selected_category = filter_var.get()

    sql = """
        SELECT id, name, amount, category, expense_date
        FROM expenses
        WHERE 1 = 1
    """
    parameters = []

    if search_text:
        sql += " AND name LIKE ?"
        parameters.append(f"%{search_text}%")

    if selected_category != "All Categories":
        sql += " AND category = ?"
        parameters.append(selected_category)

    sql += " ORDER BY id DESC"

    cursor.execute(sql, parameters)

    for row_id, name, amount, category, expense_date in cursor.fetchall():
        transaction_table.insert(
            "",
            tk.END,
            iid=str(row_id),
            values=(
                name,
                f"{amount:,.2f}",
                category,
                expense_date
            )
        )

# ---------- ADD EXPENSE ----------
def add_expense():
    name = expense_entry.get().strip()
    amount_text = amount_entry.get().strip()
    category = category_box.get()

    if not name or not amount_text:
        messagebox.showwarning(
            "Missing Information",
            "Please enter the expense name and amount.",
            parent=root
        )
        return

    try:
        amount = float(amount_text)

        if amount <= 0:
            messagebox.showwarning(
                "Invalid Amount",
                "Amount must be greater than zero.",
                parent=root
            )
            return

    except ValueError:
        messagebox.showwarning(
            "Invalid Amount",
            "Enter a valid number, such as 120 or 99.50.",
            parent=root
        )
        return

    cursor.execute("""
        INSERT INTO expenses (name, amount, category, expense_date)
        VALUES (?, ?, ?, ?)
    """, (name, amount, category, date.today().isoformat()))

    conn.commit()

    expense_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    category_box.set("Food")

    update_dashboard()

    messagebox.showinfo(
        "Expense Added",
        f"{name} saved successfully!\nAmount: ₹{amount:.2f}",
        parent=root
    )

    expense_entry.focus_set()

# ---------- SEARCH / FILTER ----------
def search_transactions():
    load_transactions()

def show_all_transactions():
    search_var.set("")
    filter_var.set("All Categories")
    load_transactions()

# ---------- DELETE SELECTED ----------
def delete_selected():
    selected_items = transaction_table.selection()

    if not selected_items:
        messagebox.showwarning(
            "No Selection",
            "Please select at least one transaction to delete.",
            parent=root
        )
        return

    confirmed = messagebox.askyesno(
        "Confirm Delete",
        f"Delete {len(selected_items)} selected transaction(s)?",
        parent=root
    )

    if not confirmed:
        return

    for item_id in selected_items:
        cursor.execute(
            "DELETE FROM expenses WHERE id = ?",
            (int(item_id),)
        )

    conn.commit()
    update_dashboard()

    messagebox.showinfo(
        "Finora",
        "Selected transaction(s) deleted successfully.",
        parent=root
    )

# ---------- EXPORT CSV ----------
def export_csv():
    cursor.execute("""
        SELECT name, amount, category, expense_date
        FROM expenses
        ORDER BY id DESC
    """)
    rows = cursor.fetchall()

    if not rows:
        messagebox.showinfo(
            "Export",
            "There are no transactions to export.",
            parent=root
        )
        return

    file_path = filedialog.asksaveasfilename(
        parent=root,
        title="Save Transactions",
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")]
    )

    if not file_path:
        return

    try:
        with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["Expense", "Amount (INR)", "Category", "Date"]
            )
            writer.writerows(rows)

        messagebox.showinfo(
            "Export Complete",
            "Transactions exported successfully.",
            parent=root
        )

    except OSError as error:
        messagebox.showerror(
            "Export Error",
            f"Could not save the file:\n{error}",
            parent=root
        )

# ---------- BUTTONS ----------
def make_button(parent, text, command, color=PURPLE):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 10, "bold"),
        bg=color,
        fg=WHITE if color != "#E9EAF5" else DARK,
        activebackground=color,
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2",
        padx=12,
        pady=7
    )

make_button(
    form, "＋ Add Expense", add_expense
).pack(anchor="w", padx=15, pady=(0, 12))

make_button(
    filter_frame, "Search / Filter", search_transactions
).pack(side="left", padx=(0, 8))

make_button(
    filter_frame, "Show All", show_all_transactions, "#E9EAF5"
).pack(side="left", padx=(0, 8))

make_button(
    filter_frame, "Delete Selected", delete_selected, RED
).pack(side="right", padx=(8, 0))

make_button(
    filter_frame, "Export CSV", export_csv
).pack(side="right", padx=(8, 0))

# ---------- SIDEBAR NAVIGATION ----------
def go_dashboard():
    show_all_transactions()
    expense_entry.focus_set()

def go_add_expense():
    expense_entry.focus_set()

def go_transactions():
    transaction_table.focus_set()

sidebar_button("▣  Dashboard", go_dashboard)
sidebar_button("＋  Add Expense", go_add_expense)
sidebar_button("☷  Transactions", go_transactions)

# ---------- KEYBOARD SHORTCUTS ----------
root.bind("<Control-f>", lambda event: search_entry.focus_set())
root.bind("<Return>", lambda event: add_expense())

# ---------- CLOSE APPLICATION ----------
def close_app():
    try:
        conn.commit()
        conn.close()
    finally:
        root.destroy()

root.protocol("WM_DELETE_WINDOW", close_app)

# ---------- START APPLICATION ----------
update_dashboard()
root.mainloop()
