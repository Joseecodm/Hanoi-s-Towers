from Node import Node

import logging
# setting logging for pass the test
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Stack:
    
    def __init__(self, limit=1000):
        self.top_item = None
        self.size = 0
        self.limit = limit
    
    def has_space(self):
        return self.size < self.limit
    
    def is_empty(self):
        return self.size == 0
    
    def peek(self):
        if not self.is_empty():
            return self.top_item.get_value()
        else:
            logger.warning("La pila esta totalmente vacia!")  # Log a warning
            return None
    
    def push(self, value):
        if self.has_space():
            item = Node(value)
            item.set_next_node(self.top_item)
            self.top_item = item
            self.size += 1
        else:
            logger.warning("La pila esta llena ¡No queda espacio!")  # Log a warning
    
    def pop(self):
        if not self.is_empty():
            item_to_remove = self.top_item
            self.top_item = item_to_remove.get_next_node()
            self.size -= 1
            return item_to_remove.get_value()
        else:
            logger.warning("La pila esta totalmente vacia!")  # Log a warning
            return None