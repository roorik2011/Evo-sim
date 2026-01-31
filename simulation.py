# simulation.py
import random
from settings import *
from agent import Agent
from plant import Plant

class Simulation:
    def __init__(self, grid_w, grid_h):
        self.gw, self.gh = grid_w, grid_h
        self.history = []
        self.explosions = []
        self.meat_storage = set()
        self.reset()

    def reset(self):
        self.grid = [[EMPTY for _ in range(self.gh)] for _ in range(self.gw)]
        self.agents = [Agent(random.randint(0, self.gw-1), random.randint(0, self.gh-1)) for _ in range(START_AGENTS)]
        # В начале спавним только "Материнские" растения (семена)
        self.plants = [Plant(random.randint(0, self.gw-1), random.randint(0, self.gh-1), True) for _ in range(START_PLANTS)]
        self.meat_storage = set()
        self.selected_agent = None
        self.history = []

    def update(self):
        self.explosions = []
        
        # 1. Позиции для логики роста
        agent_pos = {(a.x, a.y) for a in self.agents}
        plant_pos = {(p.x, p.y) for p in self.plants}
        occupied_all = agent_pos | plant_pos | self.meat_storage

        # 2. Рост растений (только "Материнские" размножаются)
        new_plants = []
        for p in self.plants:
            if p.can_reproduce and random.random() < PLANT_REPRODUCTION_CHANCE:
                child = p.try_reproduce(self.gw, self.gh, occupied_all)
                if child:
                    new_plants.append(child)
                    occupied_all.add((child.x, child.y))
        self.plants.extend(new_plants)

        # Редкий спавн новых "Материнских" растений (семян)
        if random.random() < RANDOM_PLANT_SPAWN_CHANCE:
            sx, sy = random.randint(0, self.gw-1), random.randint(0, self.gh-1)
            if (sx, sy) not in occupied_all:
                self.plants.append(Plant(sx, sy, True))

        # 3. Обновление сетки
        self.grid = [[EMPTY for _ in range(self.gh)] for _ in range(self.gw)]
        for p in self.plants: self.grid[p.x][p.y] = PLANT
        for mx, my in self.meat_storage: self.grid[mx][my] = MEAT

        # 4. Логика Агентов
        occupied_agents = {(a.x, a.y): a for a in self.agents}
        dead_agents = set()

        for a in self.agents[:]:
            if a in dead_agents: continue
            a.energy -= 0.3
            nx, ny = a.get_front_pos(self.gw, self.gh)
            target = occupied_agents.get((nx, ny))
            cell = self.grid[nx][ny]
            
            view = cell
            if target:
                diff = sum(1 for k in a.genome if a.genome[k] != target.genome[k])
                view = AGENT if diff <= 1 else "ENEMY"

            action = a.genome.get(view, 8)

            if action == 0: # MOVE
                if cell == EMPTY and (nx, ny) not in occupied_agents:
                    del occupied_agents[(a.x, a.y)]; a.x, a.y = nx, ny; occupied_agents[(a.x, a.y)] = a
            elif action == 1: a.dir = (a.dir - 1) % 4
            elif action == 2: a.dir = (a.dir + 1) % 4
            elif action == 3: # EAT
                if cell == PLANT:
                    self.plants = [p for p in self.plants if not (p.x == nx and p.y == ny)]
                    a.energy += 20
                elif cell == MEAT:
                    self.meat_storage.discard((nx, ny))
                    a.energy += 35
            elif action == 4: # ATTACK
                if target: target.energy -= 80; a.energy += 15
            elif action == 5: # REPRODUCE
                if a.energy > 100: self.spawn_child(a, occupied_agents)
            elif action == 6: # PHOTOSYNTHESIS
                a.energy += 0.7
            
            if EXPERIMENTAL_MODE:
                if action == 7: self.trigger_explosion(a, occupied_agents, dead_agents)
                elif action == 9: 
                    if target and a.energy > 1:
                        give = a.energy / 2; a.energy -= give; target.energy += give
                elif action == 10:
                    if target and target.energy > 1:
                        take = target.energy / 2; target.energy -= take; a.energy += take

            if a.energy > 200: self.spawn_child(a, occupied_agents)
            if a.energy <= 0: dead_agents.add(a)

        for a in dead_agents:
            if a in self.agents:
                if a == self.selected_agent: self.selected_agent = None
                self.meat_storage.add((a.x, a.y))
                self.agents.remove(a)
        
        self.history.append(len(self.agents))
        if len(self.history) > 200: self.history.pop(0)

    def trigger_explosion(self, owner, occupied, dead_set):
        self.explosions.append((owner.x, owner.y))
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                tx, ty = (owner.x + dx) % self.gw, (owner.y + dy) % self.gh
                self.plants = [p for p in self.plants if not (p.x == tx and p.y == ty)]
                self.meat_storage.discard((tx, ty))
                target = occupied.get((tx, ty))
                if target: dead_set.add(target)
        dead_set.add(owner)

    def spawn_child(self, parent, occupied):
        """Ребенок теперь может заменить собой растение или мясо"""
        child_energy = parent.energy / 2
        parent.energy /= 2
        offsets = [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)]
        random.shuffle(offsets)
        
        for dx, dy in offsets:
            tx, ty = (parent.x + dx) % self.gw, (parent.y + dy) % self.gh
            
            # Проверяем, нет ли там ДРУГОГО агента
            if (tx, ty) not in occupied:
                # Если там растение — удаляем его
                self.plants = [p for p in self.plants if not (p.x == tx and p.y == ty)]
                # Если там мясо — удаляем его
                self.meat_storage.discard((tx, ty))
                
                # Создаем ребенка
                child = Agent(tx, ty, parent.mutate() if random.random() < 0.15 else parent.genome, energy=child_energy)
                self.agents.append(child)
                occupied[(tx, ty)] = child
                break