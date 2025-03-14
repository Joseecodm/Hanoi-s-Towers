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
