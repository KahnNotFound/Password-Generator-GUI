import tkinter as tk
from tkinter import ttk, messagebox
import string
import random
import os

def generate_password(length, use_upper, use_numbers, use_symbols):
    chars = string.ascii_lowercase

    if use_upper:
        chars += string.ascii_uppercase
    if use_numbers:
        chars += string.digits
    if use_symbols:
        chars += "!@#$%^&*()-_=+[]{};:,.<>?/"

    return "".join(random.choice(chars) for _ in range(length))


class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Password Generator")
        self.geometry("500x400")
        self.resizable(False, False)

        # Variables
        self.length_var = tk.IntVar(value=12)
        self.upper_var = tk.BooleanVar(value=True)
        self.number_var = tk.BooleanVar(value=True)
        self.symbol_var = tk.BooleanVar(value=True)
        self.password_var = tk.StringVar(value="")

        # History list
        self.history = []

        self.create_widgets()

    def create_widgets(self):

        title_label = ttk.Label(self, text="Password Generator", font=("Segoe UI", 16, "bold"))
        title_label.pack(pady=10)

        # Options frame
        options_frame = ttk.Frame(self)
        options_frame.pack(pady=5)

        ttk.Label(options_frame, text="Password length:").grid(row=0, column=0)
        ttk.Entry(options_frame, textvariable=self.length_var, width=7).grid(row=0, column=1)

        ttk.Checkbutton(options_frame, text="Include uppercase (A-Z)", variable=self.upper_var).grid(row=1, column=0, columnspan=2, sticky="w")
        ttk.Checkbutton(options_frame, text="Include numbers (0-9)", variable=self.number_var).grid(row=2, column=0, columnspan=2, sticky="w")
        ttk.Checkbutton(options_frame, text="Include symbols (!,@,#...)", variable=self.symbol_var).grid(row=3, column=0, columnspan=2, sticky="w")

        ttk.Button(self, text="Generate Password", command=self.on_generate).pack(pady=10)

        # Generated password
        output_frame = ttk.Frame(self)
        output_frame.pack(fill="x", padx=20)

        ttk.Label(output_frame, text="Generated password:").grid(row=0, column=0, sticky="w")
        ttk.Entry(output_frame, textvariable=self.password_var, state="readonly").grid(row=1, column=0, sticky="we")

        ttk.Button(self, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(pady=5)

        # HISTORY SECTION
        history_label = ttk.Label(self, text="Password History:", font=("Segoe UI", 12, "bold"))
        history_label.pack(pady=5)

        self.history_listbox = tk.Listbox(self, height=6, width=60)
        self.history_listbox.pack()

        ttk.Button(self, text="Save History to File", command=self.save_history).pack(pady=5)

    def on_generate(self):
        try:
            length = int(self.length_var.get())
        except ValueError:
            messagebox.showerror("Error", "Password length must be a number.")
            return

        password = generate_password(
            length,
            self.upper_var.get(),
            self.number_var.get(),
            self.symbol_var.get()
        )

        self.password_var.set(password)

        # Add to history
        self.history.append(password)
        self.history_listbox.insert(tk.END, password)

    def copy_to_clipboard(self):
        pwd = self.password_var.get()
        if not pwd:
            messagebox.showinfo("Info", "No password to copy.")
            return

        self.clipboard_clear()
        self.clipboard_append(pwd)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

    def save_history(self):
        if not self.history:
            messagebox.showinfo("Info", "History is empty.")
            return

        with open("password_history.txt", "w") as f:
            for pwd in self.history:
                f.write(pwd + "\n")

        messagebox.showinfo("Saved", "History saved to password_history.txt!")


if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
