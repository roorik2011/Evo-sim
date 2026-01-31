# main.py
import pygame
from settings import * 
from simulation import Simulation

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Evo-Sim")
    font = pygame.font.SysFont("Consolas", 14)
    clock = pygame.time.Clock()
    
    grid_w = (WIDTH - UI_WIDTH) // TILE_SIZE
    grid_h = HEIGHT // TILE_SIZE
    
    sim = Simulation(grid_w, grid_h)
    speed = 10.0
    paused = False
    last_tick = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: paused = not paused
                if event.key == pygame.K_PERIOD: speed += 2.0
                if event.key == pygame.K_COMMA: speed = max(0.1, speed - 2.0)
                if event.key == pygame.K_r: sim.reset()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if event.button == 1:
                    gx, gy = mx // TILE_SIZE, my // TILE_SIZE
                    sim.selected_agent = next((a for a in sim.agents if a.x == gx and a.y == gy), None)
                elif event.button == 4: speed += 2.0
                elif event.button == 5: speed = max(0.1, speed - 2.0)

        if not paused and (current_time - last_tick > 1000 / speed):
            sim.update()
            last_tick = current_time

        screen.fill(COLORS["BG"])
        
        # Рисуем еду и мясо
        for x in range(sim.gw):
            for y in range(sim.gh):
                if sim.grid[x][y] != EMPTY:
                    pygame.draw.rect(screen, COLORS[sim.grid[x][y]], (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
        # Рисуем агентов с черным контуром
        for a in sim.agents:
            rect = (a.x*TILE_SIZE, a.y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, COLORS["AGENT"], rect)
            pygame.draw.rect(screen, COLORS["OUTLINE"], rect, 1) # ТОТ САМЫЙ КОНТУР
            if a == sim.selected_agent:
                pygame.draw.rect(screen, COLORS["SELECT"], rect, 2)

        # UI
        ui_x = WIDTH - UI_WIDTH
        pygame.draw.rect(screen, COLORS["UI"], (ui_x, 0, UI_WIDTH, HEIGHT))
        
        # График
        if len(sim.history) > 1:
            graph_h = 100
            graph_y = HEIGHT - 120
            max_pop = max(sim.history) if max(sim.history) > 0 else 1
            points = []
            for i, val in enumerate(sim.history):
                px = ui_x + 10 + (i * (UI_WIDTH - 20) / 200)
                py = graph_y + graph_h - (val / max_pop * graph_h)
                points.append((px, py))
            if len(points) > 1:
                pygame.draw.lines(screen, COLORS["GRAPH"], False, points, 2)
                
        for ex, ey in sim.explosions:
            rect = (ex*TILE_SIZE - TILE_SIZE, ey*TILE_SIZE - TILE_SIZE, TILE_SIZE*3, TILE_SIZE*3)
            pygame.draw.rect(screen, COLORS["EXPLOSION"], rect)

        ui_lines = [
            f"SPEED: {speed:.1f}x",
            f"POPULATION: {len(sim.agents)}",
            f"EXPERIMENTAL: {'ON' if EXPERIMENTAL_MODE else 'OFF'}",
            "RESTART: 'R' | PAUSE: 'Space'",
            "---------------------"
        ]
        
        if sim.selected_agent:
            a = sim.selected_agent
            ui_lines += [f"ENERGY: {int(a.energy)}", "BRAIN MAP:"]
            for k, v in a.genome.items():
                ui_lines.append(f" {VIEW_TYPES[k]}: {ACTIONS[v]}")
        
        for i, line in enumerate(ui_lines):
            screen.blit(font.render(line, True, COLORS["TEXT"]), (ui_x + 10, 20 + i * 20))

        pygame.display.flip()
        clock.tick(FPS) # Теперь FPS определен через импорт

if __name__ == "__main__":
    main()