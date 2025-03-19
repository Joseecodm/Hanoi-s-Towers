import tkinter as tk
import os
from tkinter import messagebox
from gui import GUI
from settings import SettingsWindow

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=150, height=50, radius=25, bg_color="#ADD8E6", text_color="black"):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0, cursor="hand2")  # ⬅ Cursor de manita
        
        self.command = command
        self.radius = radius
        self.bg_color = bg_color

        self.create_rounded_rectangle(0, 0, width, height, radius, fill=bg_color, outline=bg_color)
        self.text_id = self.create_text(width//2, height//2, text=text, fill=text_color, font=("Arial", 12, "normal"))

        self.bind("<Button-1>", self.on_click)
        self.tag_bind(self.text_id, "<Button-1>", self.on_click)

        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        self.create_arc(x1, y1, x1 + radius * 2, y1 + radius * 2, start=90, extent=90, **kwargs)
        self.create_arc(x2 - radius * 2, y1, x2, y1 + radius * 2, start=0, extent=90, **kwargs)
        self.create_arc(x1, y2 - radius * 2, x1 + radius * 2, y2, start=180, extent=90, **kwargs)
        self.create_arc(x2 - radius * 2, y2 - radius * 2, x2, y2, start=270, extent=90, **kwargs)
        self.create_rectangle(x1 + radius, y1, x2 - radius, y2, **kwargs)
        self.create_rectangle(x1, y1 + radius, x2, y2 - radius, **kwargs)

    def on_click(self, event=None):
        if self.command:
            self.command()

    def on_hover(self, event):
        """Cambia el cursor a una manita cuando pasa sobre el botón."""
        self.config(cursor="hand2")

    def on_leave(self, event):
        """Restaura el cursor cuando sale del botón."""
        self.config(cursor="")
import tkinter as tk
from tkinter import messagebox
from settings import SettingsWindow

class MainMenu(tk.Frame):
    def __init__(self, master, start_game_callback, exit_callback, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.start_game_callback = start_game_callback
        self.exit_callback = exit_callback
        self.num_disks = 3  # Número de discos por defecto
        self.pack(expand=True, fill='both')

        container = tk.Frame(self, bg="#F0F0F0")
        container.pack(expand=True)

        title_frame = tk.Frame(container, bg="#F0F0F0")
        title_frame.pack(pady=20)

        tk.Label(title_frame, text="H", font=("Arial", 35, "bold"), fg="#FFB3E6", bg="#F0F0F0").pack(side=tk.LEFT)
        tk.Label(title_frame, text="a", font=("Arial", 35, "bold"), fg="#D1B3FF", bg="#F0F0F0").pack(side=tk.LEFT)
        tk.Label(title_frame, text="n", font=("Arial", 35, "bold"), fg="#A7C7E7", bg="#F0F0F0").pack(side=tk.LEFT)
        tk.Label(title_frame, text="o", font=("Arial", 35, "bold"), fg="#A8E6CF", bg="#F0F0F0").pack(side=tk.LEFT)
        tk.Label(title_frame, text="i", font=("Arial", 35, "bold"), fg="#fff333", bg="#F0F0F0").pack(side=tk.LEFT)
        tk.Label(title_frame, text="'s", font=("Arial", 35, "bold"), fg="#FFABAB", bg="#F0F0F0").pack(side=tk.LEFT)

        tk.Label(title_frame, text=" ", font=("Arial", 35, "bold"), bg="#F0F0F0").pack(side=tk.LEFT)

        tk.Label(title_frame, text="T", font=("Arial", 35, "bold"), fg="#A8E6CF", bg="#F0F0F0").pack(side=tk.LEFT)
        tk.Label(title_frame, text="o", font=("Arial", 35, "bold"), fg="#FFB3E6", bg="#F0F0F0").pack(side=tk.LEFT)
        tk.Label(title_frame, text="w", font=("Arial", 35, "bold"), fg="#D1B3FF", bg="#F0F0F0").pack(side=tk.LEFT)
        tk.Label(title_frame, text="e", font=("Arial", 35, "bold"), fg="#A7C7E7", bg="#F0F0F0").pack(side=tk.LEFT)
        tk.Label(title_frame, text="r", font=("Arial", 35, "bold"), fg="#fff333", bg="#F0F0F0").pack(side=tk.LEFT)
        tk.Label(title_frame, text="s", font=("Arial", 35, "bold"), fg="#FFABAB", bg="#F0F0F0").pack(side=tk.LEFT)

        self.new_game_button = RoundedButton(container, 
                                             text="New Game", 
                                             command=lambda: self.start_game_callback(self.num_disks), 
                                             bg_color="#F0F0F0")
        self.new_game_button.pack(pady=15)

        buttons_frame = tk.Frame(container, bg="#F0F0F0")
        buttons_frame.pack(pady=10)

        self.settings_button = RoundedButton(buttons_frame, text="Settings", command=self.open_settings, bg_color="#F0F0F0")
        self.settings_button.pack(side=tk.LEFT, padx=10)

        self.tutorial_button = RoundedButton(buttons_frame, text="Tutorial", command=self.show_tutorial, bg_color="#F0F0F0")
        self.tutorial_button.pack(side=tk.LEFT, padx=10)

        self.exit_button = RoundedButton(buttons_frame, text="Exit", command=self.exit_callback, bg_color="#FF6961")
        self.exit_button.pack(side=tk.LEFT, padx=10)

    def open_settings(self):
        """Abre la ventana de configuración para cambiar el número de discos."""
        SettingsWindow(self, self.update_disks, self.num_disks)

    def update_disks(self, new_value):
        """Actualiza el número de discos basado en la configuración."""
        self.num_disks = new_value

    def show_tutorial(self):
        tutorial_text = (
            "Tutorial:\n\n"
            "El objetivo del juego es mover todos los discos de la torre izquierda a la torre derecha, siguiendo estas reglas:\n"
            "1. Solo puedes mover un disco a la vez.\n"
            "2. No puedes colocar un disco más grande sobre uno más pequeño.\n"
            "3. Usa las tres torres estratégicamente para resolver el juego en la menor cantidad de movimientos.\n\n"
            "¡Buena suerte!"
        )
        messagebox.showinfo("Tutorial", tutorial_text)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Hanoi Towers")

        width, height = 600, 400
        self.root.geometry(f"{width}x{height}")
        self.center_window(width, height)

        # Número de discos por defecto
        self.num_disks = 3

        # Crear el menú principal y pasarle la referencia a start_game
        self.main_menu = MainMenu(root, self.start_game, self.exit_game)

    def start_game(self, num_disks=None):
        """Se llama al pulsar 'New Game'. Destruye el menú y crea el juego con el número de discos seleccionado."""
        if num_disks is not None:
            self.num_disks = num_disks  # Actualizar el número de discos
        self.main_menu.destroy()
        self.game_gui = GUI(self.root, num_disks=self.num_disks)  # Pasar el número de discos

    def exit_game(self):
        """Cerrar la aplicación."""
        self.root.quit()
    
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

