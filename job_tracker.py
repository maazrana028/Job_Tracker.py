import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# Database setup
def create_table():
    conn = sqlite3.connect("job_tracker.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL,
            application_date TEXT NOT NULL,
            follow_up_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Add job application
def add_job():
    company = entry_company.get()
    role = entry_role.get()
    status = entry_status.get()
    app_date = entry_app_date.get()
    follow_up = entry_follow_up.get()

    if company and role and status and app_date:
        conn = sqlite3.connect("job_tracker.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO jobs (company, role, status, application_date, follow_up_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (company, role, status, app_date, follow_up))
        conn.commit()
        conn.close()
        clear_entries()
        refresh_table()
    else:
        messagebox.showwarning("Input Error", "Please fill all required fields.")

# Update job application
def update_job():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a job to update.")
        return

    job_id = tree.item(selected, "text")
    company = entry_company.get()
    role = entry_role.get()
    status = entry_status.get()
    app_date = entry_app_date.get()
    follow_up = entry_follow_up.get()

    if company and role and status and app_date:
        conn = sqlite3.connect("job_tracker.db")
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE jobs
            SET company=?, role=?, status=?, application_date=?, follow_up_date=?
            WHERE id=?
        ''', (company, role, status, app_date, follow_up, job_id))
        conn.commit()
        conn.close()
        clear_entries()
        refresh_table()
    else:
        messagebox.showwarning("Input Error", "Please fill all required fields.")

# Delete job application
def delete_job():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a job to delete.")
        return

    job_id = tree.item(selected, "text")
    conn = sqlite3.connect("job_tracker.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE id=?", (job_id,))
    conn.commit()
    conn.close()
    refresh_table()

# Clear input fields
def clear_entries():
    entry_company.delete(0, tk.END)
    entry_role.delete(0, tk.END)
    entry_status.delete(0, tk.END)
    entry_app_date.delete(0, tk.END)
    entry_follow_up.delete(0, tk.END)

# Refresh the table
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect("job_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, text=row[0], values=(row[1], row[2], row[3], row[4], row[5]))
    conn.close()

# GUI setup
root = tk.Tk()
root.title("Job Application Tracker")

# Input fields
tk.Label(root, text="Company").grid(row=0, column=0, padx=10, pady=10)
entry_company = tk.Entry(root)
entry_company.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Role").grid(row=1, column=0, padx=10, pady=10)
entry_role = tk.Entry(root)
entry_role.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Status").grid(row=2, column=0, padx=10, pady=10)
entry_status = tk.Entry(root)
entry_status.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Application Date").grid(row=3, column=0, padx=10, pady=10)
entry_app_date = tk.Entry(root)
entry_app_date.grid(row=3, column=1, padx=10, pady=10)

tk.Label(root, text="Follow-Up Date").grid(row=4, column=0, padx=10, pady=10)
entry_follow_up = tk.Entry(root)
entry_follow_up.grid(row=4, column=1, padx=10, pady=10)

# Buttons
tk.Button(root, text="Add Job", command=add_job).grid(row=5, column=0, padx=10, pady=10)
tk.Button(root, text="Update Job", command=update_job).grid(row=5, column=1, padx=10, pady=10)
tk.Button(root, text="Delete Job", command=delete_job).grid(row=5, column=2, padx=10, pady=10)

# Table to display jobs
columns = ("Company", "Role", "Status", "Application Date", "Follow-Up Date")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

# Initialize database and refresh table
create_table()
refresh_table()

# Run the application
root.mainloop()