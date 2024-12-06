from tkinter import *
import tkinter.scrolledtext as scrolledtext
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

# Initializing the compiler
compiler = Tk()
compiler.title("My Colorful Compiler")
compiler.geometry("900x650")
compiler.configure(bg="#1e1e2e")  # Background for a modern, dark theme

# Storing the file path
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

# Function to save a file
def save_as():
    path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    if path:
        with open(path, 'w') as file:
            code = editor.get('1.0', END)
            file.write(code)
            set_file_path(path)

# Function to run the code
def run():
    code = editor.get("1.0", END).strip()
    if not code:
        code_output.config(state=NORMAL)
        code_output.delete("1.0", END)
        code_output.insert(END, "Error: No code to execute.\n", "error")
        code_output.config(state=DISABLED)
        return

    try:
        process = subprocess.Popen(
            ["python", "-c", code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        code_output.config(state=NORMAL)
        code_output.delete("1.0", END)
        if stdout:
            code_output.insert(END, stdout)
        if stderr:
            code_output.insert(END, stderr, "error")
        code_output.config(state=DISABLED)
    except Exception as e:
        code_output.config(state=NORMAL)
        code_output.delete("1.0", END)
        code_output.insert(END, f"Error: {str(e)}", "error")
        code_output.config(state=DISABLED)

# Modern Button Style
def styled_button(text, command):
    return Button(
        button_frame,
        text=text,
        command=command,
        font=("Segoe UI", 10, "bold"),
        bg="#ff6f61",
        fg="#ffffff",
        activebackground="#ff3b2f",
        activeforeground="#ffffff",
        relief=FLAT,
        bd=0,
        padx=10,
        pady=5,
    )

# Adding Title Label
title_label = Label(
    compiler,
    text="My Colorful Python Compiler",
    font=("Segoe UI", 16, "bold"),
    bg="#1e1e2e",
    fg="#ffffff",
    pady=10
)
title_label.pack()

# Code editor area
editor_frame = Frame(compiler, bg="#1e1e2e")
editor_frame.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))

editor_label = Label(
    editor_frame,
    text="Editor",
    font=("Segoe UI", 10, "bold"),
    bg="#1e1e2e",
    fg="#ffffff",
    anchor="w"
)
editor_label.pack(fill=X, padx=5)

editor = Text(
    editor_frame,
    bg="#282a36",
    fg="#f8f8f2",
    insertbackground="#ffffff",
    font=("Consolas", 12),
    wrap=WORD,
    relief=FLAT,
    bd=5
)
editor.pack(fill=BOTH, expand=True, padx=5, pady=(0, 5))

# Output area
output_label = Label(
    compiler,
    text="Output",
    font=("Segoe UI", 10, "bold"),
    bg="#1e1e2e",
    fg="#ffffff",
    anchor="w"
)
output_label.pack(fill=X, padx=10)

output_frame = Frame(compiler, bg="#1e1e2e")
output_frame.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))

code_output = scrolledtext.ScrolledText(
    output_frame,
    bg="#282a36",
    fg="#50fa7b",
    insertbackground="#ffffff",
    font=("Consolas", 12),
    height=14,
    wrap=WORD,
    state=DISABLED,
    relief=FLAT,
    bd=5
)
code_output.pack(fill=BOTH, expand=True, padx=5, pady=(0, 5))
code_output.tag_configure("error", foreground="red")

# Button Panel
button_frame = Frame(compiler, bg="#1e1e2e")
button_frame.pack(pady=5)

open_button = styled_button("Open", open_file)
open_button.pack(side=LEFT, padx=5)

save_button = styled_button("Save", save_as)
save_button.pack(side=LEFT, padx=5)

run_button = styled_button("Run", run)
run_button.pack(side=LEFT, padx=5)

# Menu Bar
menu_bar = Menu(compiler, bg="#3a3a3a", fg="#ffffff", activebackground="#555555", activeforeground="#ffffff")
file_menu = Menu(menu_bar, tearoff=0, bg="#3a3a3a", fg="#ffffff", activebackground="#555555", activeforeground="#ffffff")
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_as)
file_menu.add_command(label='Save As', command=save_as)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=compiler.destroy)
menu_bar.add_cascade(label='File', menu=file_menu)

edit_menu = Menu(menu_bar, tearoff=0, bg="#3a3a3a", fg="#ffffff", activebackground="#555555", activeforeground="#ffffff")
edit_menu.add_command(label="Cut", command=lambda: editor.event_generate("<<Cut>>"))
edit_menu.add_command(label="Copy", command=lambda: editor.event_generate("<<Copy>>"))
edit_menu.add_command(label="Paste", command=lambda: editor.event_generate("<<Paste>>"))
menu_bar.add_cascade(label='Edit', menu=edit_menu)

run_menu = Menu(menu_bar, tearoff=0, bg="#3a3a3a", fg="#ffffff", activebackground="#555555", activeforeground="#ffffff")
run_menu.add_command(label='Run', command=run)
menu_bar.add_cascade(label='Run', menu=run_menu)

compiler.config(menu=menu_bar)

# Start the application
compiler.mainloop()
