# plant.py
import random
from settings import *

class Plant:
    def __init__(self, x, y, can_reproduce=False):
        self.x = x
        self.y = y
        self.can_reproduce = can_reproduce # Если True — это "Семечко/Мать"

    def try_reproduce(self, grid_w, grid_h, occupied_cells):
        """Материнское растение спавнит обычные растения вокруг"""
        if not self.can_reproduce:
            return None
            
        offsets = [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)]
        random.shuffle(offsets)
        
        for dx, dy in offsets:
            nx, ny = (self.x + dx) % grid_w, (self.y + dy) % grid_h
            if (nx, ny) not in occupied_cells:
                # Порождает обычное растение, которое не размножается
                return Plant(nx, ny, can_reproduce=False)
        return None