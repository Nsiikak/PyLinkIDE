import os
import tkinter as tk
from tkinter import *
import tkinter.scrolledtext as scrolledtext
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

# Silence deprecation warnings for tkinter on macOS
os.environ["TK_SILENCE_DEPRECATION"] = "1"

# Create main application window
app = Tk()
app.title("Python Compiler for macOS/Linux")
app.geometry("900x650")
app.configure(bg="#2b2b2b")  # Dark theme for modern look

# Global variable for file path
file_path = ''


# Function to set the file path
def set_file_path(path):
    global file_path
    file_path = path


# Function to open a file
def open_file():
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
    if path:
        with open(path, 'r') as file:
            code = file.read()
            editor.delete('1.0', END)
            editor.insert('1.0', code)
            set_file_path(path)


# Function to save the current file
def save_file():
    if file_path == '':
        save_as()
    else:
        with open(file_path, 'w') as file:
            code = editor.get('1.0', END)
            file.write(code)


# Function to save the file with a new name
def save_as():
    path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    if path:
        with open(path, 'w') as file:
            code = editor.get('1.0', END)
            file.write(code)
            set_file_path(path)


# Function to execute the code in the editor
def run_code():
    if not editor.get('1.0', END).strip():
        update_output("No code to execute!", "error")
        return

    try:
        process = subprocess.Popen(
            ["python3", "-c", editor.get('1.0', END)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()

        code_output.config(state=NORMAL)
        code_output.delete('1.0', END)
        if stdout:
            code_output.insert(END, stdout, "output")
        if stderr:
            code_output.insert(END, stderr, "error")
        code_output.config(state=DISABLED)
    except Exception as e:
        update_output(f"Execution Error: {e}", "error")


# Function to update the output box
def update_output(message, tag):
    code_output.config(state=NORMAL)
    code_output.delete('1.0', END)
    code_output.insert(END, message, tag)
    code_output.config(state=DISABLED)


# Modern button style
def create_button(text, command):
    return Button(
        button_frame,
        text=text,
        command=command,
        font=("Segoe UI", 10, "bold"),
        bg="#007acc",
        fg="#ffffff",
        activebackground="#005f99",
        activeforeground="#ffffff",
        padx=15,
        pady=5,
        relief=FLAT
    )


# Label for Title
title = Label(
    app,
    text="Python Compiler for macOS/Linux",
    font=("Segoe UI", 16, "bold"),
    bg="#2b2b2b",
    fg="#ffffff",
    pady=10
)
title.pack()

# Code editor
editor_frame = Frame(app, bg="#2b2b2b")
editor_frame.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))

editor_label = Label(
    editor_frame,
    text="Editor",
    font=("Segoe UI", 10, "bold"),
    bg="#2b2b2b",
    fg="#ffffff",
    anchor="w"
)
editor_label.pack(fill=X, padx=5)

editor = Text(
    editor_frame,
    bg="#1e1e1e",
    fg="#d4d4d4",
    insertbackground="#ffffff",  # Cursor color
    font=("Consolas", 12),
    wrap=WORD,
    relief=FLAT
)
editor.pack(fill=BOTH, expand=True, padx=5, pady=(0, 5))

# Output Box
output_label = Label(
    app,
    text="Output",
    font=("Segoe UI", 10, "bold"),
    bg="#2b2b2b",
    fg="#ffffff",
    anchor="w"
)
output_label.pack(fill=X, padx=10)

output_frame = Frame(app, bg="#2b2b2b")
output_frame.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))

code_output = scrolledtext.ScrolledText(
    output_frame,
    bg="#1e1e1e",
    fg="#00ff00",
    insertbackground="#ffffff",  # Cursor color
    font=("Consolas", 12),
    height=10,
    wrap=WORD,
    state=DISABLED,
    relief=FLAT
)
code_output.pack(fill=BOTH, expand=True, padx=5, pady=5)
code_output.tag_configure("error", foreground="red")
code_output.tag_configure("output", foreground="white")

# Button Frame
button_frame = Frame(app, bg="#2b2b2b")
button_frame.pack(pady=10)

open_btn = create_button("Open", open_file)
open_btn.pack(side=LEFT, padx=5)

save_btn = create_button("Save", save_file)
save_btn.pack(side=LEFT, padx=5)

save_as_btn = create_button("Save As", save_as)
save_as_btn.pack(side=LEFT, padx=5)

run_btn = create_button("Run", run_code)
run_btn.pack(side=LEFT, padx=5)

# Menu Bar
menu_bar = Menu(app, bg="#333333", fg="#ffffff", activebackground="#555555", activeforeground="#ffffff")
file_menu = Menu(menu_bar, tearoff=0, bg="#333333", fg="#ffffff", activebackground="#555555", activeforeground="#ffffff")
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=app.destroy)
menu_bar.add_cascade(label="File", menu=file_menu)

run_menu = Menu(menu_bar, tearoff=0, bg="#333333", fg="#ffffff", activebackground="#555555", activeforeground="#ffffff")
run_menu.add_command(label="Run", command=run_code)
menu_bar.add_cascade(label="Run", menu=run_menu)

app.config(menu=menu_bar)

# Start the app
app.mainloop()