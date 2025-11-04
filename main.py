import pygame_gui
from searching_algorithms import *
from grid import Grid

if __name__ == "__main__":
    pygame.init()

    FOOTER_HEIGHT = 60
    WIN = pygame.display.set_mode((WIDTH, HEIGHT + FOOTER_HEIGHT))

    manager = pygame_gui.UIManager((WIDTH, HEIGHT + FOOTER_HEIGHT))

    algo_buttons = {
        "BFS": pygame_gui.elements.UIButton(pygame.Rect(10, HEIGHT + 10, 60, 40), "BFS", manager),
        "DFS": pygame_gui.elements.UIButton(pygame.Rect(75, HEIGHT + 10, 60, 40), "DFS", manager),
        "A*": pygame_gui.elements.UIButton(pygame.Rect(140, HEIGHT + 10, 60, 40), "A*", manager),
        "UCS": pygame_gui.elements.UIButton(pygame.Rect(205, HEIGHT + 10, 60, 40), "UCS", manager),
        "Dijkstra": pygame_gui.elements.UIButton(pygame.Rect(270, HEIGHT + 10, 80, 40), "Dijk", manager),
    }

    play_button = pygame_gui.elements.UIButton(
        pygame.Rect(WIDTH - 110, HEIGHT + 10, 100, 40),
        "Play",
        manager
    )

    ROWS, COLS = 50, 50
    grid = Grid(WIN, ROWS, COLS, WIDTH, HEIGHT)

    start = None
    end = None
    run = True
    started = False
    current_algo = "BFS"
    algo_buttons[current_algo].disable()

    clock = pygame.time.Clock()

    left_drag = False

    def paint_barrier_at(pos):
        row, col = grid.get_clicked_pos(pos)
        if 0 <= row < ROWS and 0 <= col < COLS:
            spot = grid.grid[row][col]
            if spot != start and spot != end:
                spot.make_barrier()

    while run:
        time_delta = clock.tick(60) / 1000.0

        grid.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            manager.process_events(event)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element in algo_buttons.values():
                    # detect which algo clicked
                    for name, btn in algo_buttons.items():
                        if btn == event.ui_element:
                            current_algo = name
                    # update enable/disable
                    for name, btn in algo_buttons.items():
                        btn.enable()
                    algo_buttons[current_algo].disable()

                elif event.ui_element == play_button:
                    if start and end:
                        started = True
                        for row in grid.grid:
                            for spot in row:
                                spot.update_neighbors(grid.grid)

                        if current_algo == 'BFS':
                            bfs(lambda: grid.draw(), grid, start, end)
                        elif current_algo == 'DFS':
                            dfs(lambda: grid.draw(), grid, start, end)
                        elif current_algo == 'A*':
                            astar(lambda: grid.draw(), grid, start, end)
                        elif current_algo == 'UCS':
                            ucs(lambda: grid.draw(), grid, start, end)
                        elif current_algo == 'Dijkstra':
                            dijkstra(lambda: grid.draw(), grid, start, end)

                        started = False

            if started:
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and event.button in (1, 3):
                pos = pygame.mouse.get_pos()
                if pos[1] > HEIGHT:
                    continue

                row, col = grid.get_clicked_pos(pos)
                if row < 0 or row >= ROWS or col < 0 or col >= COLS:
                    continue

                spot = grid.grid[row][col]

                if event.button == 1:  # LEFT
                    left_drag = True
                    if not start and spot != end:
                        start = spot
                        start.make_start()
                    elif not end and spot != start:
                        end = spot
                        end.make_end()
                    elif spot != end and spot != start:
                        spot.make_barrier()

            if event.type == pygame.MOUSEMOTION:
                if event.pos[1] <= HEIGHT:
                    if left_drag:
                        paint_barrier_at(event.pos)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    left_drag = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    print("Clearing the grid...")
                    start = None
                    end = None
                    grid.reset()

        pygame.draw.rect(WIN, (35, 35, 35), (0, HEIGHT, WIDTH, FOOTER_HEIGHT))

        manager.update(time_delta)
        manager.draw_ui(WIN)

        pygame.display.update()

    pygame.quit()
