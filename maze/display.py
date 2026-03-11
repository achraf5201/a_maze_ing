from typing import Any, List, Tuple, Optional

class Display:
    """Class for rendering mazes, reading maze data, and displaying solutions.

    Attributes:
        START_COLOR (str): Color for the maze background.
        FORTY2_COLOR (str): Color for the reserved 42-shaped area.
        WALL_COLOR (str): Color for maze walls.
        PATH_COLOR (str): Color for empty paths.
        SOLVE_COLOR (str): Color for solution path.
        RESET (str): ANSI reset code for colors.
    """
    def __init__(
            self,
            color_wall: str = '\033[107m',
            forty2_color: str = '\033[100m'
    ) -> None:
        """Initializes display colors for maze rendering."""
        self.START_COLOR = '\033[49m'
        self.FORTY2_COLOR = forty2_color
        self.WALL_COLOR = color_wall
        self.PATH_COLOR = '\033[49m'
        self.SOLVE_COLOR = '\033[48;5;94m'
        self.RESET = '\033[0m'

    def read_hex(self, filename: str) -> List[List[int]]:
        """Reads a maze grid from a file in hexadecimal format."""
        try:
            mylist = []
            with open(filename, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or "," in line:
                        break
                    new_line = []
                    for c in line:
                        try:
                            new_line.append(int(c, 16))
                        except ValueError:
                            continue
                    if new_line:
                        mylist.append(new_line)
                return mylist
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []
        except Exception as e:
            print(f"Error reading bit map: {e}")
            return []

    def read_dir(self, filename: str) -> str:
        """Reads the solution path directions from a maze file."""
        try:
            flag = 0
            with open(filename, "r") as f:
                for line in f:
                    if "," in line:
                        flag = 1
                    if flag == 1:
                        if "," not in line and line.strip():
                            return line.strip()
                return ""
        except Exception as e:
            print(f"Error reading direction: {e}")
            return ""

    def draw(
            self,
            array: List[List[Any]], 
            width: int, 
            height: int,
            entry: Tuple[int, int], 
            exit_node: Tuple[int, int],
            solve: Optional[List[Tuple[int, int]]] = None,
            fla: int = 1
    ) -> List[str]:
        """Draws the maze as a list of strings with colors."""
        if solve is None:
            solve = []

        canvas_h = height * 2 + 1
        canvas_w = width * 2 + 1
        
        # Initialize canvas with walls (1)
        matrix = [[1 for _ in range(canvas_w)] for _ in range(canvas_h)]
        
        for y in range(height):
            for x in range(width):
                if y < len(array) and x < len(array[y]):
                    cell = array[y][x]
                    cy = y * 2 + 1
                    cx = x * 2 + 1
                    matrix[cy][cx] = 0 # Center of cell is empty
                    
                    # Bitmask logic: 1=N, 2=S, 4=E, 8=W (Example assumption)
                    # Adjusting based on standard maze generation bitmasks:
                    # Usually: 1=N, 2=S, 4=E, 8=W
                    if not (cell & 1): matrix[cy-1][cx] = 0 # North
                    if not (cell & 2): matrix[cy+1][cx] = 0 # South
                    if not (cell & 4): matrix[cy][cx+1] = 0 # East
                    if not (cell & 8): matrix[cy][cx-1] = 0 # West
                    
                    if (cell & 1) and (cell & 2) and (cell & 4) and (cell & 8):
                         matrix[cy][cx] = 2 # Special block (42)

        output = []
        solve_pixels = set()
        
        # Calculate solution path pixels if requested (odd flag)
        if fla % 2 != 0 and solve:
            curr_x, curr_y = entry
            # Ensure solve path starts correctly; solve list usually contains next steps
            for next_y, next_x in solve:
                p1_r = 2 * curr_y + 1
                p1_c = 2 * curr_x + 1
                p2_r = 2 * next_y + 1
                p2_c = 2 * next_x + 1

                solve_pixels.add((p2_r, p2_c))
                mid_r = (p1_r + p2_r) // 2
                mid_c = (p1_c + p2_c) // 2
                solve_pixels.add((mid_r, mid_c))
                # Add start point too
                solve_pixels.add((p1_r, p1_c))
                curr_y, curr_x = next_y, next_x

        for r in range(canvas_h):
            line = ""
            for c in range(canvas_w):
                is_wall = matrix[r][c] == 1
                is_42 = matrix[r][c] == 2
                is_entry = (r == entry[1] * 2 + 1 and c == entry[0] * 2 + 1)
                is_exit = (r == exit_node[1] * 2 + 1 and c == exit_node[0] * 2 + 1)
                
                is_solve = False
                if fla % 2 != 0:
                    is_solve = (r, c) in solve_pixels

                if is_wall:
                    line += f"{self.WALL_COLOR}  {self.RESET}"
                elif is_entry:
                    line += f"{self.START_COLOR}🚕{self.RESET}"
                elif is_exit:
                    line += f"🏁{self.RESET}"
                elif is_42:
                    line += f"{self.FORTY2_COLOR}  {self.RESET}"
                elif is_solve:
                    line += f"{self.SOLVE_COLOR}  {self.RESET}"
                else:
                    line += f"{self.PATH_COLOR}  {self.RESET}"
            output.append(line)
        return output

    def create_solve_cor(
            self, entry: Tuple[int, int], directions: str) -> List[Tuple[int, int]]:
        """Converts a string of directions into a list of coordinates."""
        x, y = entry
        mylist = []
        for char in directions:
            if char == 'S':
                y += 1
            elif char == 'N':
                y -= 1
            elif char == 'W':
                x -= 1
            elif char == 'E':
                x += 1
            mylist.append((y, x)) # Storing as (row, col) i.e., (y, x)
        return mylist