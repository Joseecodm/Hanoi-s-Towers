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
        # Draw disks
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
