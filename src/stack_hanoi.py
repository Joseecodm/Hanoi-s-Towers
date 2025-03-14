class Stack:
    def __init__(self, name):
        """Initialize a new stack with the given name."""
        self.name = name
        self.items = []
        
    def push(self, item):
        """Add an item to the top of the stack."""
        self.items.append(item)

    def pop(self):
        """Remove and return the top item of the stack."""
        if self.items:
            return self.items.pop()
        raise IndexError("Pop from empty stack")
