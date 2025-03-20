import tkinter as tk 
from tkinter import messagebox
from stack_hanoi import Stack

class GUI:
    def __init__(self, root, num_disks=3, return_to_menu_callback=None):
        self.root = root
        self.root.title("Tower of Hanoi")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.return_to_menu_callback = return_to_menu_callback  # Callback to return to the menu

        self.num_disks = num_disks
        self.stacks = [Stack("Left"), Stack("Middle"), Stack("Right")]
        self.selected_disk = None
        self.origin_stack = None
        self.num_moves = 0
        self.offset_x = 0
        self.offset_y = 0

        # Canvas for drawing the game
        self.canvas = tk.Canvas(root, width=600, height=350, bg="white", highlightthickness=0)
        self.canvas.pack()

        # Frame for buttons (top left)
        button_frame = tk.Frame(root, bg="white")
        button_frame.place(x=10, y=10)

        # Button to return to the menu
        self.back_button = tk.Button(button_frame, text="Back", command=self.back_to_menu, bg="#FF6961",
                                     font=("Arial", 10, "bold"), fg="white", width=6, height=1, relief="ridge")
        self.back_button.pack(side=tk.LEFT, padx=5)

        # Reset button
        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset_game, bg="#A8E6CF",
                                      font=("Arial", 10, "bold"), width=6, height=1, relief="ridge")
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Moves counter (bottom)
        self.moves_label = tk.Label(root, text="Moves: 0", font=("Arial", 12, "bold"), bg="white")
        self.moves_label.pack(side=tk.BOTTOM, pady=5)

        self.reset_game()

    def back_to_menu(self):
        """Return to the main menu."""
        if self.return_to_menu_callback:
            self.root.destroy()  # Close the game window
            self.return_to_menu_callback()  # Execute the callback

    def reset_game(self):
        """Reset the game and redraw the interface."""
        self.stacks = [Stack("Left"), Stack("Middle"), Stack("Right")]
        for i in range(self.num_disks, 0, -1):
            self.stacks[0].push(i)
        self.num_moves = 0
        self.selected_disk = None
        self.origin_stack = None
        self.moves_label.config(text="Moves: 0")
        self.draw_game()

    def draw_game(self):
        """Draw the towers and disks."""
        self.canvas.delete("all")

        # Draw towers
        for i in range(3):
            x = 100 + i * 200
            self.canvas.create_rectangle(x - 5, 150, x + 5, 350, fill="black")

        # Draw disks on each tower
        for stack_index, stack in enumerate(self.stacks):
            x = 100 + stack_index * 200
            y = 350
            for disk in stack.get_all_items():
                width = 20 * disk
                color = self.get_disk_color(disk)
                self.canvas.create_rectangle(
                    x - width // 2, y - 20, x + width // 2, y,
                    fill=color, outline="black", tags=f"disk_{disk}"
                )
                y -= 20

        # Update moves counter
        self.moves_label.config(text=f"Moves: {self.num_moves}")

        # Bind mouse events to enable dragging of disks
        for disk in range(1, self.num_disks + 1):
            self.canvas.tag_bind(f"disk_{disk}", "<Button-1>", self.start_drag)
            self.canvas.tag_bind(f"disk_{disk}", "<B1-Motion>", self.during_drag)
            self.canvas.tag_bind(f"disk_{disk}", "<ButtonRelease-1>", self.stop_drag)

    def get_disk_color(self, disk):
        """Return a color for the disk based on its size."""
        colors = ["red", "green", "blue", "yellow", "orange", "purple", "pink", "cyan"]
        return colors[(disk - 1) % len(colors)]

    def start_drag(self, event):
        """Start dragging a disk."""
        x, y = event.x, event.y
        for stack_idx, stack in enumerate(self.stacks):
            if stack.get_size() > 0:
                top_disk = stack.get_all_items()[-1]
                disk_coords = self.canvas.coords(f"disk_{top_disk}")
                if disk_coords:
                    x1, y1, x2, y2 = disk_coords
                    if x1 <= x <= x2 and y1 <= y <= y2:
                        self.selected_disk = top_disk
                        self.origin_stack = stack_idx
                        self.offset_x = x - x1  # Adjust click offset
                        self.offset_y = y - y1
                        return

    def during_drag(self, event):
        """Move the disk while dragging."""
        if self.selected_disk:
            width = 20 * self.selected_disk
            new_x1 = event.x - self.offset_x
            new_x2 = new_x1 + width
            self.canvas.coords(f"disk_{self.selected_disk}", new_x1, event.y - 10, new_x2, event.y + 10)

    def stop_drag(self, event):
        """Stop dragging and drop the disk if the move is valid."""
        if not self.selected_disk:
            return
        x = event.x
        for stack_idx in range(3):
            stack_center = 100 + stack_idx * 200
            if stack_center - 50 <= x <= stack_center + 50:
                if self.is_valid_move(self.origin_stack, stack_idx):
                    self.move_disk(self.origin_stack, stack_idx)
                else:
                    self.draw_game()
                self.selected_disk = None
                return
        self.draw_game()
        self.selected_disk = None

    def is_valid_move(self, origin_idx, dest_idx):
        """Check if the move is valid."""
        if origin_idx == dest_idx:
            return False
        origin_stack = self.stacks[origin_idx]
        dest_stack = self.stacks[dest_idx]
        if origin_stack.get_size() == 0:
            return False
        moving_disk = origin_stack.get_all_items()[-1]
        if dest_stack.get_size() == 0:
            return True
        dest_top_disk = dest_stack.get_all_items()[-1]
        return moving_disk < dest_top_disk

    def move_disk(self, origin_idx, dest_idx):
        """Move a disk and update the game interface."""
        disk = self.stacks[origin_idx].pop()
        self.stacks[dest_idx].push(disk)
        self.num_moves += 1
        self.draw_game()
        if self.check_win():
            messagebox.showinfo("You Won!", f"Completed the game in {self.num_moves} moves!")

    def check_win(self):
        """Check if the game is won."""
        return self.stacks[2].get_size() == self.num_disks
