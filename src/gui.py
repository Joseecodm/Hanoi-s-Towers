import tkinter as tk
from tkinter import messagebox
from stack_hanoi import Stack

class GUI:
    def __init__(self, root, num_disks=3):
        self.root = root
        self.root.title("Tower of Hanoi")

        self.num_disks = num_disks
        self.stacks = [Stack("Left"), Stack("Middle"), Stack("Right")]
        self.selected_disk = None
        self.origin_stack = None
        self.num_moves = 0

        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()

        control_frame = tk.Frame(root)
        control_frame.pack()
        tk.Label(control_frame, text="Number of Disks:").pack(side=tk.LEFT)
        self.difficulty = tk.IntVar(value=self.num_disks)
        tk.OptionMenu(control_frame, self.difficulty, *range(3, 9), command=self.set_difficulty).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Reset", command=self.reset_game).pack(side=tk.LEFT)

        self.reset_game()

    def set_difficulty(self, _):
        """Adjust the number of disks and reset the game."""
        self.num_disks = self.difficulty.get()
        self.reset_game()

    def reset_game(self):
        """Reset the game and redraw the interface."""
        self.stacks = [Stack("Left"), Stack("Middle"), Stack("Right")]
        for i in range(self.num_disks, 0, -1):
            self.stacks[0].push(i)
        self.num_moves = 0
        self.selected_disk = None
        self.origin_stack = None
        self.draw_game()

    def draw_game(self):
        """Draw the stacks and disks on the canvas."""
        self.canvas.delete("all")
        # Draw stacks
        for i in range(3):
            x = 100 + i * 200
            self.canvas.create_rectangle(x - 5, 150, x + 5, 350, fill="black")
        # Draw disks in each stack
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
        # Bind events for dragging disks
        for disk in range(1, self.num_disks + 1):
            self.canvas.tag_bind(f"disk_{disk}", "<Button-1>", self.start_drag)
            self.canvas.tag_bind(f"disk_{disk}", "<B1-Motion>", self.during_drag)
            self.canvas.tag_bind(f"disk_{disk}", "<ButtonRelease-1>", self.stop_drag)
        # Show move counter
        self.canvas.create_text(300, 20, text=f"Moves: {self.num_moves}", font=("Arial", 16), fill="black")

    def get_disk_color(self, disk):
        """Return a color for the disk based on its size."""
        colors = ["red", "green", "blue", "yellow", "orange", "purple", "pink", "cyan"]
        return colors[(disk - 1) % len(colors)]

    def is_valid_move(self, origin_idx, dest_idx):
        """Check if moving the top disk from origin stack to destination stack is valid."""
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
        """Move the top disk from origin stack to destination stack and update the game."""
        disk = self.stacks[origin_idx].pop()
        self.stacks[dest_idx].push(disk)
        self.num_moves += 1
        self.draw_game()
        if self.check_win():
            messagebox.showinfo("You Won!", f"Completed the game in {self.num_moves} moves!")

    def check_win(self):
        """Check if the game is won (all disks moved to the right stack)."""
        return self.stacks[2].get_size() == self.num_disks

    def start_drag(self, event):
        """Initiate the dragging of a disk."""
        x, y = event.x, event.y
        for stack_idx, stack in enumerate(self.stacks):
            if stack.get_size() > 0:
                top_disk = stack.get_all_items()[-1]
                disk_coords = self.canvas.coords(f"disk_{top_disk}")
                if disk_coords and (disk_coords[0] <= x <= disk_coords[2] and disk_coords[1] <= y <= disk_coords[3]):
                    self.selected_disk = top_disk
                    self.origin_stack = stack_idx
                    return

    def during_drag(self, event):
        """Update the position of the disk during dragging."""
        if self.selected_disk:
            width = 20 * self.selected_disk
            new_x1 = event.x - width / 2
            new_x2 = event.x + width / 2
            self.canvas.coords(f"disk_{self.selected_disk}", new_x1, event.y - 10, new_x2, event.y + 10)

    def stop_drag(self, event):
        """Finish dragging the disk and attempt a move."""
        if not self.selected_disk:
            return
        x = event.x
        for stack_idx in range(3):
            stack_center = 100 + stack_idx * 200
            if stack_center - 50 <= x <= stack_center + 50:
                if self.is_valid_move(self.origin_stack, stack_idx):
                    self.move_disk(self.origin_stack, stack_idx)
                else:
                    self.draw_game()  # Restore position if move is invalid
                self.selected_disk = None
                return
        self.draw_game()
        self.selected_disk = None

if __name__ == '__main__':
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
