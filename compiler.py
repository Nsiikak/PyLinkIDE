import subprocess
import os
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename

# Function to set file path
file_path = ""

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

# Function to save file
def save_file():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
        if path:
            set_file_path(path)
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)

# Function to run code
def run_code():
    if file_path == '':
        save_prompt = Toplevel()
        Label(save_prompt, text="Please save your code before running").pack()
        return
    command = f"python3 {file_path}"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    output_field.delete('1.0', END)
    output_field.insert('1.0', output.decode())
    output_field.insert('1.0', error.decode())

# Tkinter GUI setup
compiler = Tk()
compiler.title('Python IDE')
compiler.geometry('700x500')

menu_bar = Menu(compiler)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_file)
file_menu.add_command(label='Exit', command=exit)
menu_bar.add_cascade(label='File', menu=file_menu)

run_menu = Menu(menu_bar, tearoff=0)
run_menu.add_command(label='Run', command=run_code)
menu_bar.add_cascade(label='Run', menu=run_menu)

compiler.config(menu=menu_bar)

editor = Text(compiler, wrap='word')
editor.pack(fill=BOTH, expand=1)

output_field = Text(height=10)
output_field.pack()

compiler.mainloop()
