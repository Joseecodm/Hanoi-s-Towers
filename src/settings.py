import tkinter as tk
from tkinter import ttk

class SettingsWindow(tk.Toplevel):
    def __init__(self, master, apply_callback, current_disks=3):
        """
        Configuration window to select the number of disks.
        
        :param master: Parent window.
        :param apply_callback: Function to apply the changes.
        :param current_disks: Currently selected number of disks.
        """
        super().__init__(master)
        self.apply_callback = apply_callback
        self.current_disks = tk.IntVar(value=current_disks)

        self.title("Settings")
        self.geometry("300x200")
        self.resizable(False, False)

        # Center the window
        self.center_window(300, 200)

        # Label for disk selection
        tk.Label(self, text="Select number of disks:", font=("Arial", 12)).pack(pady=10)

        # Spinbox to choose number of disks
        self.disk_selector = ttk.Spinbox(self, from_=3, to=8, textvariable=self.current_disks, width=5, font=("Arial", 12))
        self.disk_selector.pack(pady=10)

        # Button to apply settings
        apply_button = tk.Button(self, text="Apply", command=self.apply_settings, font=("Arial", 12), bg="#A8E6CF")
        apply_button.pack(pady=20)

    def apply_settings(self):
        """Apply the settings and close the window."""
        self.apply_callback(self.current_disks.get())
        self.destroy()

    def center_window(self, width, height):
        """Center the window on the screen."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
