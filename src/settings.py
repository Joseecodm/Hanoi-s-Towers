import tkinter as tk
from tkinter import ttk

class SettingsWindow(tk.Toplevel):
    def __init__(self, master, apply_callback, current_disks=3):
        """
        Ventana de configuración para seleccionar el número de discos.
        
        :param master: Ventana principal.
        :param apply_callback: Función que aplicará los cambios.
        :param current_disks: Número de discos actualmente seleccionado.
        """
        super().__init__(master)
        self.apply_callback = apply_callback
        self.current_disks = tk.IntVar(value=current_disks)

        self.title("Settings")
        self.geometry("300x200")
        self.resizable(False, False)

        # Centrar la ventana
        self.center_window(300, 200)

        # Etiqueta
        tk.Label(self, text="Select number of disks:", font=("Arial", 12)).pack(pady=10)

        # Selector de número de discos
        self.disk_selector = ttk.Spinbox(self, from_=3, to=8, textvariable=self.current_disks, width=5, font=("Arial", 12))
        self.disk_selector.pack(pady=10)

        # Botón para aplicar los cambios
        apply_button = tk.Button(self, text="Apply", command=self.apply_settings, font=("Arial", 12), bg="#A8E6CF")
        apply_button.pack(pady=20)

    def apply_settings(self):
        """Aplica la configuración y cierra la ventana."""
        self.apply_callback(self.current_disks.get())  # Envía el valor seleccionado al menú principal
        self.destroy()

    def center_window(self, width, height):
        """Centra la ventana en la pantalla."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
