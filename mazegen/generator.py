import random
import sys
from collections import deque
from typing import Deque, Any


class MazeGenerator:
    """Generates and solves mazes using depth-first search (DFS).

    Attributes:
        width (int): Width of the maze.
        height (int): Height of the maze.
        grid (List[List[int]]): 2D grid representing the maze,
        walls encoded as bits.
        visited (List[List[bool]]): 2D grid tracking visited cells
        during generation.
    """
    def __init__(self, width: int, height: int) -> None:
        """Initializes the maze grid and visited matrix.

        Args:
            width (int): Width of the maze.
            height (int): Height of the maze.
        """
        self.width: int = width
        self.height: int = height
        self.grid: list[list[int]] = [
            [15 for _ in range(width)]
            for _ in range(height)
        ]
        self.visited: list[list[bool]] = [
            [False for _ in range(width)]
            for _ in range(height)
        ]

    def remove_wall(
            self, x1: int, y1: int, x2: int, y2: int
    ) -> None:
        """Removes the wall between two adjacent cells.

        Args:
            x1 (int): X-coordinate of the first cell.
            y1 (int): Y-coordinate of the first cell.
            x2 (int): X-coordinate of the second cell.
            y2 (int): Y-coordinate of the second cell.
        """
        dx: int = x2 - x1
        dy: int = y2 - y1
        if dx == 1:
            self.grid[y1][x1] &= ~2
            self.grid[y2][x2] &= ~8
        elif dx == -1:
            self.grid[y1][x1] &= ~8
            self.grid[y2][x2] &= ~2
        elif dy == 1:
            self.grid[y1][x1] &= ~4
            self.grid[y2][x2] &= ~1
        elif dy == -1:
            self.grid[y1][x1] &= ~1
            self.grid[y2][x2] &= ~4

    def generate_42(
            self, exit: tuple[Any, Any], entry: tuple[Any, Any]) -> None:
        """Reserves a 42-shaped pattern in the maze center.

        Args:
            exit (Tuple[int, int]): Coordinates of the maze exit.
            entry (Tuple[int, int]): Coordinates of the maze entry.

        Raises:
            Exception: If the entry or exit is inside the reserved 42 zone.
        """
        y = (self.height // 2) - (5 // 2)
        x = (self.width // 2) - (7 // 2)
        matrix_42 = [
            [(0, 0), (0, 4), (0, 5), (0, 6)],
            [(1, 0), (1, 6)],
            [(2, 0), (2, 1), (2, 2), (2, 4), (2, 5), (2, 6)],
            [(3, 2), (3, 4)],
            [(4, 2), (4, 4), (4, 5), (4, 6)]
        ]
        exit_x, exit_y = exit[0] - x, exit[1] - y
        entry_x, entry_y = entry[0] - x, entry[1] - y
        for cor in matrix_42:
            if (exit_y, exit_x) in cor:
                raise Exception("Invalid maze: exit is inside the 42 zone")
            if (entry_y, entry_x) in cor:
                raise Exception("Invalid maze: entry is inside the 42 zone")
        for i in matrix_42:
            for tup in i:
                self.visited[y + tup[0]][x + tup[1]] = True

    def get_nextors(self, x: int, y: int) -> list[Any]:
        """Returns a list of unvisited neighboring cells.

        Args:
            x (int): X-coordinate of the current cell.
            y (int): Y-coordinate of the current cell.

        Returns:
            List[Tuple[int, int]]: Coordinates of unvisited neighboring cells.
        """
        mylist: list[tuple[int, int]] = []
        if x - 1 >= 0:
            if not self.visited[y][x - 1]:
                mylist.append((y, x - 1))
        if y - 1 >= 0:
            if not self.visited[y - 1][x]:
                mylist.append((y - 1, x))
        if x + 1 < self.width:
            if not self.visited[y][x + 1]:
                mylist.append((y, x + 1))
        if y + 1 < self.height:
            if not self.visited[y + 1][x]:
                mylist.append((y + 1, x))
        return mylist

    def dfs_algo(self, x: int, y: int) -> None:
        """Generates the maze recursively using depth-first search.

        Args:
            x (int): X-coordinate of the current cell.
            y (int): Y-coordinate of the current cell.
        """
        self.visited[y][x] = True
        nextors: list[tuple[int, int]] = self.get_nextors(x, y)
        random.shuffle(nextors)
        for ny, nx in nextors:
            if not self.visited[ny][nx]:
                self.remove_wall(x, y, nx, ny)
                self.dfs_algo(nx, ny)

    def solve(
        self, start_x: int, start_y: int, end_x: int, end_y: int
    ) -> list[str]:
        """Solves the maze using breadth-first search.

        Args:
            start_x (int): X-coordinate of the start cell.
            start_y (int): Y-coordinate of the start cell.
            end_x (int): X-coordinate of the exit cell.
            end_y (int): Y-coordinate of the exit cell.

        Returns:
            List[str]: Sequence of directions
            ('N', 'S', 'E', 'W') from start to exit.
        """
        queue: Deque[tuple[int, int, list[Any]]] = deque(
            [(start_x, start_y, [])]
        )
        visited: set[tuple[int, int]] = set()
        visited.add((start_x, start_y))
        while queue:
            x, y, path = queue.popleft()
            if x == end_x and y == end_y:
                return path
            current_cell = self.grid[y][x]
            move = [
                (0, -1, 'N', 1),
                (1, 0, 'E', 2),
                (0, 1, 'S', 4),
                (-1, 0, 'W', 8)
            ]
            for dx, dy, dir, wall_bit in move:
                nx = x + dx
                ny = y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not (current_cell & wall_bit):
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            new_path: list[str] = path + [dir]
                            queue.append((nx, ny, new_path))
        return []

    def write_in_file(self, param: dict, file_output: str) -> None:
        """Writes the maze, entry/exit, and solution path to a file.

        Args:
            param (dict): Maze configuration containing 'ENTRY' and 'EXIT'.
            file_output (str): File path to write the maze and solution.
        """
        try:
            with open(file_output, "w") as fo:
                for row in self.grid:
                    fo.write(
                        "".join(str(hex(cell)[2:]).upper() for cell in row))
                    fo.write("\n")
                fo.write(f"\n{param['ENTRY'][0]},{param['ENTRY'][1]}\n")
                fo.write(f"{param['EXIT'][0]},{param['EXIT'][1]}\n")
                mylist = self.solve(param['ENTRY'][0], param['ENTRY'][1],
                                    param['EXIT'][0], param['EXIT'][1])
                fo.write("".join(mylist) + "\n")
        except Exception:
            print(f"ERROR: Cannot open the file {file_output}")

    def run_dfs(self, param: dict) -> None:
        """Resets visited cells and runs DFS to generate the maze.

        Args:
            param (dict): Dictionary containing 'ENTRY' and 'EXIT'.
        """
        self.visited = [
            [False for _ in range(self.width)] for _ in range(self.height)]
        if self.height >= 12 and self.width >= 11:
            self.generate_42(param["EXIT"], param["ENTRY"])
        self.dfs_algo(param["ENTRY"][0], param["ENTRY"][1])

    def main_generator(
            self, param: dict, file_output: str, check: int) -> None:
        """Main function to generate the maze and write it to file.

        Args:
            param (dict): Maze configuration parameters.
            file_output (str): Output file path.
            check (int): Seed flag; if 1, random seed is fixed
            for reproducibility.
        """
        if check:
            random.seed(1)
        try:
            if not param["PERFECT"]:
                self.run_dfs(param)
            self.run_dfs(param)
            self.write_in_file(param, file_output)
        except Exception as e:
            print(e)
            sys.exit()
