import random
import sys
from collections import deque
from typing import Deque, List, Tuple, Any, Dict, Set


class MazeGenerator:
    """Generates and solves mazes using depth-first search (DFS).

    Attributes:
        width (int): Width of the maze.
        height (int): Height of the maze.
        grid (List[List[int]]): 2D grid representing the maze,
                                walls encoded as bits (N=1, S=2, E=4, W=8).
        visited (List[List[bool]]): 2D grid tracking visited cells
                                    during generation.
    """

    def __init__(self, width: int, height: int) -> None:
        """Initializes the maze grid and visited matrix."""
        self.width: int = width
        self.height: int = height
        # Initialize grid with all walls present (1+2+4+8 = 15)
        self.grid: List[List[int]] = [
            [15 for _ in range(width)]
            for _ in range(height)
        ]
        self.visited: List[List[bool]] = [
            [False for _ in range(width)]
            for _ in range(height)
        ]

    def remove_wall(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """Removes the wall between two adjacent cells.
        
        Bitmask Convention (must match display.py):
        North = 1, South = 2, East = 4, West = 8
        """
        if not (0 <= x1 < self.width and 0 <= y1 < self.height) or \
           not (0 <= x2 < self.width and 0 <= y2 < self.height):
            return

        dx: int = x2 - x1
        dy: int = y2 - y1

        if dx == 1:  # Moving East: Remove East from (x1,y1) and West from (x2,y2)
            self.grid[y1][x1] &= ~4
            self.grid[y2][x2] &= ~8
        elif dx == -1:  # Moving West: Remove West from (x1,y1) and East from (x2,y2)
            self.grid[y1][x1] &= ~8
            self.grid[y2][x2] &= ~4
        elif dy == 1:  # Moving South: Remove South from (x1,y1) and North from (x2,y2)
            self.grid[y1][x1] &= ~2
            self.grid[y2][x2] &= ~1
        elif dy == -1:  # Moving North: Remove North from (x1,y1) and South from (x2,y2)
            self.grid[y1][x1] &= ~1
            self.grid[y2][x2] &= ~2

    def generate_42(self, exit_node: Tuple[int, int], entry: Tuple[int, int]) -> None:
        """Reserves a 42-shaped pattern in the maze center by marking it visited."""
        # 42 pattern dimensions approx 5x7
        y_offset = (self.height // 2) - 2
        x_offset = (self.width // 2) - 3
        
        # Coordinates relative to the offset where walls should remain (visited=True)
        matrix_42 = [
            # 4 shape
            (0, 0), (0, 4), (0, 5), (0, 6),
            (1, 0), (1, 6),
            (2, 0), (2, 1), (2, 2), (2, 4), (2, 5), (2, 6),
            (3, 2), (3, 4),
            (4, 2), (4, 4), (4, 5), (4, 6)
        ]

        exit_x, exit_y = exit_node
        entry_x, entry_y = entry

        reserved_cells = []
        for r, c in matrix_42:
            abs_y = y_offset + r
            abs_x = x_offset + c
            
            if 0 <= abs_y < self.height and 0 <= abs_x < self.width:
                reserved_cells.append((abs_y, abs_x))
                if (abs_x, abs_y) == (entry_x, entry_y):
                    raise Exception("Invalid maze: entry is inside the 42 zone")
                if (abs_x, abs_y) == (exit_x, exit_y):
                    raise Exception("Invalid maze: exit is inside the 42 zone")

        # Mark as visited so DFS doesn't carve into them -> they remain walls
        for r, c in reserved_cells:
            self.visited[r][c] = True

    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Returns a list of unvisited neighboring cells (y, x)."""
        neighbors: List[Tuple[int, int]] = []
        # Check West
        if x - 1 >= 0 and not self.visited[y][x - 1]:
            neighbors.append((y, x - 1))
        # Check North
        if y - 1 >= 0 and not self.visited[y - 1][x]:
            neighbors.append((y - 1, x))
        # Check East
        if x + 1 < self.width and not self.visited[y][x + 1]:
            neighbors.append((y, x + 1))
        # Check South
        if y + 1 < self.height and not self.visited[y + 1][x]:
            neighbors.append((y + 1, x))
        return neighbors

    def dfs_algo(self, x: int, y: int) -> None:
        """Generates the maze recursively using depth-first search."""
        self.visited[y][x] = True
        neighbors = self.get_neighbors(x, y)
        random.shuffle(neighbors)
        
        for ny, nx in neighbors:
            if not self.visited[ny][nx]:
                self.remove_wall(x, y, nx, ny)
                self.dfs_algo(nx, ny)

    def solve(
        self, start_x: int, start_y: int, end_x: int, end_y: int
    ) -> List[str]:
        """Solves the maze using breadth-first search (BFS).
        
        Returns:
            List[str]: Sequence of directions ('N', 'S', 'E', 'W').
        """
        # Queue stores: (x, y, path_list)
        queue: Deque[Tuple[int, int, List[str]]] = deque([(start_x, start_y, [])])
        visited: Set[Tuple[int, int]] = set()
        visited.add((start_x, start_y))

        while queue:
            x, y, path = queue.popleft()
            
            if x == end_x and y == end_y:
                return path

            current_cell = self.grid[y][x]
            
            # Moves: (dx, dy, direction_char, wall_bit_to_check)
            # North=1, South=2, East=4, West=8
            moves = [
                (0, -1, 'N', 1), # North
                (0, 1, 'S', 2),  # South
                (1, 0, 'E', 4),  # East
                (-1, 0, 'W', 8)  # West
            ]

            for dx, dy, direction, wall_bit in moves:
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    # Check if wall exists in that direction
                    # If bit is 0, wall is open
                    if not (current_cell & wall_bit):
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            new_path = path + [direction]
                            queue.append((nx, ny, new_path))
        return []

    def write_in_file(self, param: Dict[str, Any], file_output: str) -> None:
        """Writes the maze, entry/exit, and solution path to a file."""
        try:
            with open(file_output, "w") as fo:
                # Write Maze Grid Hex
                for row in self.grid:
                    # Convert int to hex string without '0x'
                    hex_line = "".join(f"{cell:x}".upper() for cell in row)
                    fo.write(hex_line + "\n")
                
                # Write Entry/Exit
                entry = param['ENTRY']
                exit_node = param['EXIT']
                fo.write(f"\n{entry[0]},{entry[1]}\n")
                fo.write(f"{exit_node[0]},{exit_node[1]}\n")
                
                # Write Solution
                solution_path = self.solve(entry[0], entry[1], exit_node[0], exit_node[1])
                fo.write("".join(solution_path) + "\n")
                
        except IOError as e:
            print(f"ERROR: Cannot open or write to file {file_output}: {e}")

    def run_dfs(self, param: Dict[str, Any]) -> None:
        """Resets visited cells and runs DFS to generate the maze."""
        # Reset visited grid for new pass
        self.visited = [
            [False for _ in range(self.width)] for _ in range(self.height)
        ]
        
        # Apply 42 mask if size permits
        if self.height >= 12 and self.width >= 11:
            try:
                self.generate_42(param["EXIT"], param["ENTRY"])
            except Exception as e:
                print(f"Warning: Could not generate 42 zone: {e}")
        
        # Run DFS
        self.dfs_algo(param["ENTRY"][0], param["ENTRY"][1])

    def main_generator(
            self, param: Dict[str, Any], file_output: str, check: int) -> None:
        """Main function to generate the maze and write it to file."""
        if check:
            random.seed(1)
        
        try:
            # If not perfect, run once to create paths, then reset visited 
            # and run again to create loops (remove more walls)
            if not param.get("PERFECT", True):
                self.run_dfs(param)
            
            # Final generation pass
            self.run_dfs(param)
            
            self.write_in_file(param, file_output)
            
        except RecursionError:
            print("Error: Maze size too large for default recursion limit.")
            sys.setrecursionlimit(max(sys.getrecursionlimit(), self.width * self.height))
            # Retry once
            self.run_dfs(param)
            self.write_in_file(param, file_output)
        except Exception as e:
            print(f"Generator Error: {e}")
            sys.exit(1)