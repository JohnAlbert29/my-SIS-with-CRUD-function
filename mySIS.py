import tkinter as tk
from tkinter import messagebox
import os
import random

def encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
            elif char.islower():
                if shifted > ord('z'):
                    shifted -= 26
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text

def decrypt(text, shift):
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) - shift
            if char.isupper():
                if shifted < ord('A'):
                    shifted += 26
            elif char.islower():
                if shifted < ord('a'):
                    shifted += 26
            decrypted_text += chr(shifted)
        else:
            decrypted_text += char
    return decrypted_text

def read_encrypted_data():
    encrypted_data = []
    if os.path.exists("encrypted.txt"):
        with open("encrypted.txt", "r") as file:
            for line in file:
                encrypted_data.append(line.strip())
    return encrypted_data

def write_encrypted_data(data):
    with open("encrypted.txt", "w") as file:
        for line in data:
            file.write(line + '\n')

def change_key():
    global encryption_key
    new_key = entry_key.get()
    if new_key.isdigit():
        encryption_key = int(new_key)
        messagebox.showinfo("Success", "Encryption key changed successfully!", parent=key_window)
        key_window.destroy()
    else:
        messagebox.showerror("Error", "Please enter a valid integer key!", parent=key_window)

def add_info():
    name = entry_name.get()
    roll = entry_roll.get()
    section = entry_section.get()
    course = entry_course.get()
    professor = entry_professor.get()
    if name and roll and section and course and professor:
        if roll.isdigit():  
            encrypted_roll = encrypt(roll, encryption_key)  
            info = f"Name: {name}, Roll: {encrypted_roll}, Section: {section}, Course: {course}, Professor: {professor}"
            encrypted_info = encrypt(info, encryption_key)  # Encrypt entire info string
            encrypted_data = read_encrypted_data()
            encrypted_data.append(encrypted_info)
            write_encrypted_data(encrypted_data)
            messagebox.showinfo("Success", "Information added successfully!", parent=root)
            # Clearing entry fields
            entry_name.delete(0, tk.END)
            entry_roll.delete(0, tk.END)
            entry_section.delete(0, tk.END)
            entry_course.delete(0, tk.END)
            entry_professor.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter a numeric roll number!", parent=root)
    else:
        messagebox.showerror("Error", "Please enter all fields!", parent=root)

def update_info():
    encrypted_data = read_encrypted_data()
    if not encrypted_data:
        messagebox.showinfo("Error", "There are no added information yet!", parent=root)
        return

    roll_to_update = entry_roll.get()
    new_name = entry_name.get()
    new_section = entry_section.get()
    new_course = entry_course.get()
    new_professor = entry_professor.get()
    if roll_to_update and new_name and new_section and new_course and new_professor:
        roll_exists = False
        updated_data = []
        for line in encrypted_data:
            decrypted_line = decrypt(line, encryption_key)
            if f"Roll: {roll_to_update}" in decrypted_line:
                roll_exists = True
                # Extract existing information and update it
                existing_info = decrypted_line.split(", ")
                existing_name = existing_info[0][len("Name: "):]
                existing_section = existing_info[1][len("Section: "):]
                existing_course = existing_info[2][len("Course: "):]
                existing_professor = existing_info[3][len("Professor: "):]
                updated_info = f"Name: {new_name}, Roll: {roll_to_update}, Section: {new_section}, Course: {new_course}, Professor: {new_professor}"
                updated_data.append(encrypt(updated_info, encryption_key))
            else:
                updated_data.append(line)
        if not roll_exists:
            messagebox.showinfo("Error", "There is no such roll number.", parent=root)
            return
        write_encrypted_data(updated_data)
        messagebox.showinfo("Success", "Information updated successfully!", parent=root)
        entry_name.delete(0, tk.END)
        entry_roll.delete(0, tk.END)
        entry_section.delete(0, tk.END)
        entry_course.delete(0, tk.END)
        entry_professor.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please enter all fields!", parent=root)

def delete_info():
    encrypted_data = read_encrypted_data()
    if not encrypted_data:
        messagebox.showinfo("Error", "There are no added information yet!", parent=root)
        return

    roll_to_delete = entry_roll.get()
    if roll_to_delete:
        roll_exists = False
        for line in encrypted_data:
            if f"Roll: {roll_to_delete}" in decrypt(line, encryption_key):
                roll_exists = True
                break
        if not roll_exists:
            messagebox.showinfo("Error", "There is no such roll number.", parent=root)
            return
        remaining_data = []
        for line in encrypted_data:
            if f"Roll: {roll_to_delete}" not in decrypt(line, encryption_key):
                remaining_data.append(line)
        write_encrypted_data(remaining_data)
        messagebox.showinfo("Success", "Information deleted successfully!", parent=root)
        entry_name.delete(0, tk.END)
        entry_roll.delete(0, tk.END)
        entry_section.delete(0, tk.END)
        entry_course.delete(0, tk.END)
        entry_professor.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please enter the roll number to delete!", parent=root)

def view_info():
    # Create a new window for entering roll number
    roll_window = tk.Toplevel(root)
    roll_window.title("Enter Roll Number")
    roll_window.geometry("300x150")

    # Function to handle viewing information after roll number entry
    def view_info_handler():
        entered_roll = entry_roll_number.get()
        encrypted_data = read_encrypted_data()
        if encrypted_data:
            decrypted_data = [decrypt(line, encryption_key) for line in encrypted_data]

            found = False
            for data in decrypted_data:
                if f"Roll: {entered_roll}" in data:
                    found = True
                    # Custom dialog for viewing information
                    view_window = tk.Toplevel(root)
                    view_window.title("View Information")
                    view_window.geometry("400x300")

                    table_frame = tk.Frame(view_window)
                    table_frame.pack(padx=10, pady=10)

                    for i, line in enumerate(data.split(", ")):
                        label = tk.Label(table_frame, text=line, font=("Helvetica", 12))
                        label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            if not found:
                messagebox.showinfo("Error", "Roll number not found.", parent=roll_window)
        else:
            messagebox.showinfo("Information", "No information available!", parent=roll_window)

    label_roll_number = tk.Label(roll_window, text="Enter Roll Number:", font=("Helvetica", 14))
    label_roll_number.pack(pady=5)

    entry_roll_number = tk.Entry(roll_window, font=("Helvetica", 14))
    entry_roll_number.pack(pady=5)

    btn_view_roll = tk.Button(roll_window, text="View Information", command=view_info_handler, bg="#009688", fg="#fff", font=("Helvetica", 14))
    btn_view_roll.pack(pady=5)

def change_bg_color():
    colors = ["#fce4ec", "#ffccbc", "#ffe0b2", "#fff9c4", "#b2ebf2", "#ff8a65", "#00acc1"]
    root.configure(bg=random.choice(colors))

def open_key_window():
    global key_window
    key_window = tk.Toplevel(root)
    key_window.title("Change Encryption Key")
    key_window.geometry("300x150")

    label_key = tk.Label(key_window, text="Enter New Key:", font=("Helvetica", 14))
    label_key.pack(pady=5)

    global entry_key
    entry_key = tk.Entry(key_window, font=("Helvetica", 14))
    entry_key.pack(pady=5)

    btn_change_key = tk.Button(key_window, text="Change Key", command=change_key, bg="#4CAF50", fg="#fff", font=("Helvetica", 14))
    btn_change_key.pack(pady=5)

# GUI setup
root = tk.Tk()
root.title("Student Information System")
root.geometry("500x600")
root.configure(bg="WhiteSmoke")  # Setting a colorful background for the window

encryption_key = 5  # Initial encryption key

title_label = tk.Label(root, text="Student Information System", fg="Black", font=("Times New Roman", 25, "italic"))
title_label.pack(pady=10)

frame = tk.Frame(root, bg="#fff")
frame.pack(padx=20, pady=20)

label_name = tk.Label(frame, text="Name:", bg="#fff", font=("Times New Roman", 18))
label_name.grid(row=1, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame, font=("Times New Roman", 18))
entry_name.grid(row=1, column=1, padx=5, pady=5)
entry_name.config(bg="#fce4ec") 

label_roll = tk.Label(frame, text="Roll:", bg="#fff", font=("Times New Roman", 18))
label_roll.grid(row=2, column=0, padx=5, pady=5)
entry_roll = tk.Entry(frame, font=("Times New Roman", 18))
entry_roll.grid(row=2, column=1, padx=5, pady=5)
entry_roll.config(bg="#ffccbc")

label_section = tk.Label(frame, text="Section:", bg="#fff", font=("Times New Roman", 18))
label_section.grid(row=3, column=0, padx=5, pady=5)
entry_section = tk.Entry(frame, font=("Times New Roman", 18))
entry_section.grid(row=3, column=1, padx=5, pady=5)
entry_section.config(bg="#ffe0b2")

label_course = tk.Label(frame, text="Course:", bg="#fff", font=("Times New Roman", 18))
label_course.grid(row=4, column=0, padx=5, pady=5)
entry_course = tk.Entry(frame, font=("Times New Roman", 18))
entry_course.grid(row=4, column=1, padx=5, pady=5)
entry_course.config(bg="#fff9c4") 

label_professor = tk.Label(frame, text="Professor:", bg="#fff", font=("Times New Roman", 18))
label_professor.grid(row=5, column=0, padx=5, pady=5)
entry_professor = tk.Entry(frame, font=("Times New Roman", 18))
entry_professor.grid(row=5, column=1, padx=5, pady=5)
entry_professor.config(bg="#b2ebf2")

btn_add = tk.Button(frame, text="Add Information", command=add_info, bg="#4CAF50", fg="#fff", font=("Times New Roman", 18))
btn_add.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="we")

btn_update = tk.Button(frame, text="Update Information", command=update_info, bg="#2196F3", fg="#fff", font=("Times New Roman", 18))
btn_update.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="we")

btn_delete = tk.Button(frame, text="Delete Information", command=delete_info, bg="#F44336", fg="#fff", font=("Times New Roman", 18))
btn_delete.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="we")

btn_view = tk.Button(frame, text="View Information", command=view_info, bg="#009688", fg="#fff", font=("Times New Roman", 18))
btn_view.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="we")

btn_add.configure(command=lambda: [change_bg_color(), add_info()])
btn_update.configure(command=lambda: [change_bg_color(), update_info()])
btn_delete.configure(command=lambda: [change_bg_color(), delete_info()])
btn_view.configure(command=lambda: [change_bg_color(), view_info()])

btn_change_key = tk.Button(root, text="Change Encryption Key", command=open_key_window, bg="#ff8a65", fg="#fff", font=("Times New Roman", 18))
btn_change_key.pack(pady=10)

def list_decrypted_data():
    encrypted_data = read_encrypted_data()
    if not encrypted_data:
        messagebox.showinfo("Error", "There are no added information yet!", parent=root)
        return

    decrypted_data_list = []
    for line in encrypted_data:
        decrypted_line = decrypt(line, encryption_key)
        decrypted_data_list.append(decrypted_line)

    # Display decrypted data
    decrypted_data_window = tk.Toplevel(root)
    decrypted_data_window.title("Decrypted Data")
    decrypted_data_window.geometry("500x400")

    scrollbar = tk.Scrollbar(decrypted_data_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(decrypted_data_window, yscrollcommand=scrollbar.set, font=("Helvetica", 12))
    for item in decrypted_data_list:
        listbox.insert(tk.END, item)
    listbox.pack(fill=tk.BOTH, expand=True)

    scrollbar.config(command=listbox.yview)

root = tk.Tk()
root.title("Student Information System")
root.geometry("500x600")
root.configure(bg="WhiteSmoke")  


title_label = tk.Label(root, text="Student Information System", fg="Black", font=("Times New Roman", 25, "italic"))
title_label.pack(pady=10)

frame = tk.Frame(root, bg="#fff")
frame.pack(padx=20, pady=20)

btn_change_key = tk.Button(frame, text="Change Encryption Key", command=open_key_window, bg="#ff8a65", fg="#fff", font=("Times New Roman", 18))
btn_change_key.grid(row=10, column=0, columnspan=2, padx=5, pady=5, sticky="we")

btn_list_decrypted_data = tk.Button(frame, text="List Decrypted Data", command=list_decrypted_data, bg="#00acc1", fg="#fff", font=("Times New Roman", 18))
btn_list_decrypted_data.grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky="we")

root.mainloop()


