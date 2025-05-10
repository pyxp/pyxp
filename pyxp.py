import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import customtkinter
from CTkMenuBar import *
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator
import subprocess
import os
import tempfile
import sys

class PyXPIDE(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("PyXP IDE")
        self.geometry("900x600")

        self.set_icon()  # Set the icon here

        self.tabs = []
        self.create_menu()
        self.create_tab_system()
        self.add_new_tab()

    def set_icon(self):
        # Use .ico for Windows via iconbitmap
        if os.name == "nt":  # Windows
            try:
                self.iconbitmap("ICON.ico")
            except Exception as e:
                print(f"Failed to load .ico icon: {e}")
        else:
            # Use .png as fallback for macOS/Linux (not ideal for Windows)
            try:
                icon = tk.PhotoImage(file="icon.png")
                self.iconphoto(False, icon)
            except Exception as e:
                print(f"Failed to load .png icon: {e}")

    def create_menu(self):
        menu = CTkTitleMenu(self)

        file_button = menu.add_cascade("File")
        file_dropdown = CustomDropdownMenu(widget=file_button)
        file_dropdown.add_option("New Tab", self.add_new_tab)
        file_dropdown.add_option("Open File", self.open_file)
        file_dropdown.add_option("Save File", self.save_file)
        file_dropdown.add_option("Run Code", self.run_code)
        file_dropdown.add_option("Exit", self.quit)

        pip_button = menu.add_cascade("Pip")
        pip_dropdown = CustomDropdownMenu(widget=pip_button)
        pip_dropdown.add_option("Install Package", self.install_package)

        pyxp_button = menu.add_cascade("PyXP")
        pyxp_dropdown = CustomDropdownMenu(widget=pyxp_button)
        pyxp_dropdown.add_option("Dark Mode", lambda: self.set_theme("dark"))
        pyxp_dropdown.add_option("Light Mode", lambda: self.set_theme("light"))

        help_button = menu.add_cascade("Help")
        help_dropdown = CustomDropdownMenu(widget=help_button)
        help_dropdown.add_option("About", self.show_about)

    def create_tab_system(self):
        self.style = ttk.Style()
        self.style.theme_use('default')

        self.style.configure('TNotebook', background="#1e1e1e", borderwidth=0)
        self.style.configure('TNotebook.Tab', background="#2d2d2d", foreground="white", padding=[12, 6])
        self.style.map('TNotebook.Tab', background=[("selected", "#3a3a3a")])

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

    def add_new_tab(self):
        frame = ttk.Frame(self.notebook, style="TFrame")
        text_widget = tk.Text(
            frame,
            wrap='none',
            undo=True,
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
            selectbackground="#555555"
        )
        text_widget.pack(expand=True, fill="both")

        # Syntax highlight
        Percolator(text_widget).insertfilter(ColorDelegator())

        tab_title = f"Untitled {len(self.tabs) + 1}"
        self.notebook.add(frame, text=tab_title)
        self.tabs.append((frame, text_widget))
        self.notebook.select(len(self.tabs) - 1)

    def get_current_text_widget(self):
        index = self.notebook.index(self.notebook.select())
        return self.tabs[index][1]

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if path:
            with open(path, "r") as file:
                content = file.read()
            self.add_new_tab()
            editor = self.get_current_text_widget()
            editor.delete("1.0", tk.END)
            editor.insert(tk.END, content)
            self.notebook.tab("current", text=os.path.basename(path))

    def save_file(self):
        editor = self.get_current_text_widget()
        content = editor.get("1.0", tk.END)
        path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
        if path:
            with open(path, "w") as file:
                file.write(content)

    def install_package(self):
        package = simpledialog.askstring("Install Package", "Enter package name:")
        if package:
            subprocess.run(["pip", "install", package])

    def show_about(self):
        messagebox.showinfo("About PyXP", "PyXP IDE\nLightweight Python IDE\n Copyright (C) 2025 Zohan Haque\n Thank you for using PyXP")

    def set_theme(self, mode):
        customtkinter.set_appearance_mode(mode)
        if mode == "dark":
            self.style.configure('TNotebook', background="#1e1e1e")
            self.style.configure('TNotebook.Tab', background="#2d2d2d", foreground="white")
            self.style.map('TNotebook.Tab', background=[("selected", "#3a3a3a")])
        else:
            self.style.configure('TNotebook', background="white")
            self.style.configure('TNotebook.Tab', background="#e0e0e0", foreground="black")
            self.style.map('TNotebook.Tab', background=[("selected", "#cccccc")])

    def run_code(self):
        editor = self.get_current_text_widget()
        code = editor.get("1.0", tk.END)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(code.encode())
            temp_file.close()

            if os.name == 'nt':  # Windows
                subprocess.Popen(['start', 'cmd', '/k', 'python', temp_file.name], shell=True)
            else:
                subprocess.Popen(['gnome-terminal', '--', 'python3', temp_file.name])

if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")
    app = PyXPIDE()
    app.mainloop()
