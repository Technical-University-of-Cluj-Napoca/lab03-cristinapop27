import heapq
import sys
from typing import List

from utils import *
from collections import deque
from queue import PriorityQueue
from grid import Grid
from spot import Spot
import math

def bfs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    if start is None or end is None:
        return False

    queue = deque([start])
    visited = {start}
    came_from = {}

    while queue:
        current = queue.popleft()

        if current == end:
            while current in came_from:
                current = came_from[current]
                current.make_path()
                draw()
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor in visited or neighbor.is_barrier():
                continue
            visited.add(neighbor)
            came_from[neighbor] = current
            queue.append(neighbor)
            neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False


def dfs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    if start is None or end is None: return False

    stack = [start]
    visited = {start}
    came_from = {}

    for event in pygame.event.get():
        if event.type is pygame.QUIT: pygame.quit()

    while stack:
        current = stack.pop()
        if current == end:
            while current in came_from:
                current = came_from[current]
                current.make_path()
                draw()
            end.make_end()
            start.make_start()
            return True

        for neighbour in current.neighbors:
            if neighbour not in visited and not neighbour.is_barrier():
                visited.add(neighbour)
                came_from[neighbour] = current
                stack.append(neighbour)
                neighbour.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False


def h_manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    """
    Heuristic function for A* algorithm: uses the Manhattan distance between two points.
    Args:
        p1 (tuple[int, int]): The first point (x1, y1).
        p2 (tuple[int, int]): The second point (x2, y2).
    Returns:
        float: The Manhattan distance between p1 and p2.
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def h_euclidian_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    """
    Heuristic function for A* algorithm: uses the Euclidian distance between two points.
    Args:
        p1 (tuple[int, int]): The first point (x1, y1).
        p2 (tuple[int, int]): The second point (x2, y2).
    Returns:
        float: The Manhattan distance between p1 and p2.
    """
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def astar(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    A* Pathfinding Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    count = 0
    open_heap = PriorityQueue()
    open_heap.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid.grid for spot in row}
    g_score[start] = 0

    f_score = {spot: float("inf") for row in grid.grid for spot in row}
    f_score[start] = h_manhattan_distance(start.get_position(), end.get_position())

    open_set = {start}
    while not open_heap.empty():
        _, _, current = open_heap.get()
        open_set.remove(current)

        if current == end:
            while current in came_from:
                current = came_from[current]
                current.make_path()
                draw()
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score+ h_manhattan_distance(neighbor.get_position(), end.get_position())
                if neighbor not in open_set:
                    count += 1
                    open_heap.put((f_score[neighbor], count, neighbor))
                    open_set.add(neighbor)
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False

def dls(draw: callable, grid: Grid, start: Spot, end: Spot, depth_limit: int) -> bool:
    if start is None or end is None: return False

    stack = [(start,0)]
    came_from = {}
    best_depth = {start:0}
    while stack:
        current, depth = stack.pop()
        if current == end:
            while current in came_from:
                current = came_from[current]
                current.make_path()
                draw()
            end.make_end()
            start.make_start()
            return True

        if depth == depth_limit:
            draw()
            if current != start:
                current.make_closed()
            continue

        for neighbor in current.neighbors:
            if depth+1 <= depth_limit and (neighbor not in best_depth or depth+1 < best_depth[neighbor]):
                best_depth[neighbor] = depth+1
                came_from[neighbor] = current
                stack.append((neighbor, depth+1))
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
    return False

def ids(draw: callable, grid: Grid,start: Spot, end: Spot) -> bool:
    if start is None or end is None: return False

    for limit in range(1,100):
        found = dls(draw, grid, start, end, limit)
        if found:
            return True
    return False

def dijkstra(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    if start is None or end is None: return False

    dist = {spot: float("inf") for row in grid.grid for spot in row}
    dist[start] = 0
    came_from = {}
    queue = PriorityQueue()
    queue.put((dist[start], start))
    while not queue.empty():
        _, current = queue.get()

        for neighbor in current.neighbors:
            temp_dist = dist[current] + 1
            if temp_dist < dist[neighbor]:
                dist[neighbor] = temp_dist
                came_from[neighbor] = current
                neighbor.make_open()
                queue.put((dist[neighbor], neighbor))
        draw()
        if current != start:
            current.make_closed()

    if dist[end] != float("inf"):
        current = end
        while current in came_from:
            current = came_from[current]
            current.make_path()
            draw()
        end.make_end()
        start.make_start()
        return True

    return False

def ucs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    if start is None or end is None: return False

    dist = {spot: float("inf") for row in grid.grid for spot in row}
    dist[start] = 0
    came_from = {}
    queue = PriorityQueue()
    queue.put((dist[start], start))
    while not queue.empty():
        _, current = queue.get()

        if current == end:
            while current in came_from:
                current = came_from[current]
                current.make_path()
                draw()
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_dist = dist[current] + 1
            if temp_dist < dist[neighbor]:
                dist[neighbor] = temp_dist
                came_from[neighbor] = current
                neighbor.make_open()
                queue.put((dist[neighbor], neighbor))
        draw()
        if current != start:
            current.make_closed()
    return False