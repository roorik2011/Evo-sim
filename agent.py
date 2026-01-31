# agent.py
import random
import copy
from settings import *

class Agent:
    def __init__(self, x, y, genome=None, energy=60):
        self.x, self.y = x, y
        self.dir = random.randint(0, 3)
        self.energy = energy # Теперь энергия может передаваться от родителя
        
        if genome:
            self.genome = genome
        else:
            self.genome = {t: random.randint(0, len(ACTIONS)-1) for t in [EMPTY, PLANT, MEAT, AGENT, "ENEMY"]}

    def mutate(self):
        new_genome = copy.deepcopy(self.genome)
        k = random.choice(list(new_genome.keys()))
        new_genome[k] = random.randint(0, len(ACTIONS)-1)
        return new_genome

    def get_front_pos(self, grid_w, grid_h): # Добавили параметры сетки
        dx, dy = [(0,-1), (1,0), (0,1), (-1,0)][self.dir]
        return (self.x + dx) % grid_w, (self.y + dy) % grid_h