import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from faker import Faker
import os

current_row = 0

def generate_dummy_data():
    faker = Faker()
    try:
        num_rows = int(num_rows_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number of rows.")
        return

    data = {}
    for col_name, data_type in column_info.items():
        if data_type == 'Name':
            data[col_name] = [faker.name() for _ in range(num_rows)]
        elif data_type == 'Age':
            data[col_name] = [faker.random_int(min=18, max=100) for _ in range(num_rows)]
        elif data_type == 'Address':
            data[col_name] = [faker.address() for _ in range(num_rows)]
        elif data_type == 'Email':
            data[col_name] = [faker.email() for _ in range(num_rows)]
        elif data_type == 'Phone':
            data[col_name] = [faker.phone_number() for _ in range(num_rows)]
        elif data_type == 'Job':
            data[col_name] = [faker.job() for _ in range(num_rows)]
        elif data_type == 'Company':
            data[col_name] = [faker.company() for _ in range(num_rows)]
        elif data_type == 'Credit Card Number':
            data[col_name] = [faker.credit_card_number() for _ in range(num_rows)]
        elif data_type == 'Date':
            data[col_name] = [faker.date_of_birth() for _ in range(num_rows)]

    df = pd.DataFrame(data)

    file_name = file_name_entry.get()
    if not file_name.endswith('.csv'):
        file_name += '.csv'
    df.to_csv(file_name, index=False)

    messagebox.showinfo("Success", "Dummy data generated and saved successfully!")

def close_splash():
    splash_window.destroy()
    root.deiconify()

def add_row():
    global current_row
    column_name = column_name_entry.get()
    data_type = column_type_var.get()

    if column_name and data_type:
        column_info[column_name] = data_type
        current_row += 1
    else:
        messagebox.showerror("Error", "Please enter both column name and type.")
        return
    column_name_entry.delete(0, tk.END)

def show_generated_data():
    file_name = file_name_entry.get()
    if not file_name.endswith('.csv'):
        file_name += '.csv'

    if os.path.exists(file_name):
        df = pd.read_csv(file_name)

        data_window = tk.Toplevel(root)
        data_window.title("Generated Data")

        tree_frame = tk.Frame(data_window)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(tree_frame)
        tree["columns"] = tuple(df.columns)
        tree.heading("#0", text="Index", anchor="w")
        for col in df.columns:
            tree.heading(col, text=col, anchor="w")

        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        tree.configure(yscrollcommand=tree_scroll.set)

        for index, row in df.iterrows():
            tree.insert("", tk.END, text=index, values=tuple(row))

        tree.pack(expand=tk.YES, fill=tk.BOTH)
    else:
        messagebox.showerror("Error", f"File {file_name} does not exist.")

splash_window = tk.Tk()
splash_window.title("Dummy Data Generator")
splash_window.geometry("400x400")

app_name_label = tk.Label(splash_window, text="Dummy Data Generator", font=("Arial", 20))
app_name_label.pack(pady=20)

developer_info_label = tk.Label(splash_window, text="Developed by:\nKhan Namrah\nKader Luqman\nUmesh Phulare", font=("Arial", 12))
developer_info_label.pack(pady=20)

close_button = tk.Button(splash_window, text="Start", command=close_splash)
close_button.pack(pady=20)

root = tk.Tk()
root.title("Dummy Data Generator")
root.withdraw()

column_types = ['Name', 'Age', 'Address', 'Email', 'Phone', 'Job', 'Company', 'Credit Card Number', 'Date']

column_info = {}
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10)

column_name_label = tk.Label(input_frame, text="Column Name:")
column_name_label.grid(row=0, column=0, padx=5, pady=5)

column_name_entry = tk.Entry(input_frame)
column_name_entry.grid(row=0, column=1, padx=5, pady=5)

column_type_label = tk.Label(input_frame, text="Column Type:")
column_type_label.grid(row=0, column=2, padx=5, pady=5)

column_type_var = tk.StringVar(root)
column_type_var.set(column_types[0])
column_type_dropdown = tk.OptionMenu(input_frame, column_type_var, *column_types)
column_type_dropdown.grid(row=0, column=3, padx=5, pady=5)

add_row_button = tk.Button(root, text="Add Row", command=add_row)
add_row_button.pack(pady=5)

file_num_frame = tk.Frame(root)
file_num_frame.pack(pady=10)

file_name_label = tk.Label(file_num_frame, text="File Name:")
file_name_label.grid(row=0, column=0, padx=5, pady=5)
file_name_entry = tk.Entry(file_num_frame)
file_name_entry.grid(row=0, column=1, padx=5, pady=5)

num_rows_label = tk.Label(file_num_frame, text="Number of Rows:")
num_rows_label.grid(row=1, column=0, padx=5, pady=5)
num_rows_entry = tk.Entry(file_num_frame)
num_rows_entry.grid(row=1, column=1, padx=5, pady=5)

generate_button = tk.Button(root, text="Generate Dummy Data", command=generate_dummy_data)
generate_button.pack(pady=10)

show_data_button = tk.Button(root, text="Show Generated Data", command=show_generated_data)
show_data_button.pack(pady=10)

root.mainloop()
