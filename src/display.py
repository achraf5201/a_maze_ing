from typing import Any


class display:
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
        """Initializes display colors for maze rendering.

        Args:
            color_wall (str, optional): Color code for walls.
            Defaults to white background.
            forty2_color (str, optional): Color code for 42-area.
            Defaults to dark gray background.
        """
        self.START_COLOR = '\033[49m'
        self.FORTY2_COLOR = forty2_color
        self.WALL_COLOR = color_wall
        self.PATH_COLOR = '\033[49m'
        self.SOLVE_COLOR = '\033[48;5;94m'
        self.RESET = '\033[0m'

    def read_hex(self, filename: str) -> list[Any]:
        """Reads a maze grid from a file in hexadecimal format.

        Args:
            filename (str): Path to the maze file.

        Returns:
            List[List[int]]: 2D list representing the maze grid.
            Empty list if an error occurs.
        """
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
        except Exception as e:
            print(f"Error reading bit map: {e}")
            return []

    def read_dir(self, filename: str) -> str:
        """Reads the solution path directions from a maze file.

        Args:
            filename (str): Path to the maze file.

        Returns:
            str: String of directions ('N', 'S', 'E', 'W').
            Empty string if not found or error occurs.
        """
        try:
            flag = 0
            with open(filename, "r") as f:
                for line in f:
                    if "," in line:
                        flag = 1
                    if flag == 1:
                        if "," not in line:
                            return line.strip()
                return ""
        except Exception as e:
            print(e)
            return ""

    def draw(
            self,
            array: list[list[Any]], width: int, height: int,
            entry: tuple[Any, Any], exit_node: tuple[Any, Any],
            solve: list[tuple[Any, Any]],
            fla: int = 1
    ) -> list[str]:
        """Draws the maze as a list of strings with colors
        and optional solution path.

        Args:
            array (List[List[Any]]): Maze grid with wall information.
            width (int): Maze width.
            height (int): Maze height.
            entry (Tuple[int, int]): Entry coordinates.
            exit_node (Tuple[int, int]): Exit coordinates.
            solve (List[Tuple[int, int]], optional): List of solution
            coordinates. Defaults to [(0,0)].
            fla (int, optional): Flag to show/hide solution path.
            Defaults to 1.

        Returns:
            List[str]: List of strings representing colored
            maze rows for terminal output.
        """
        canvas_h = height * 2 + 1
        canvas_w = width * 2 + 1
        matrix = [
            [1 for _ in range(canvas_w)] for _ in range(canvas_h)]
        for y in range(height):
            for x in range(width):
                cell = array[y][x]
                cy = y * 2 + 1
                cx = x * 2 + 1
                matrix[cy][cx] = 0
                if not (cell & 1):
                    matrix[cy-1][cx] = 0
                if not (cell & 2):
                    matrix[cy][cx+1] = 0
                if not (cell & 4):
                    matrix[cy+1][cx] = 0
                if not (cell & 8):
                    matrix[cy][cx-1] = 0
                if (cell & 1) and (cell & 2) and (cell & 4) and (cell & 8):
                    matrix[cy][cx] = 2
        output = []
        solve_pixels = set()
        curr_x, curr_y = entry
        if fla % 2:
            for next_y, next_x in solve:
                p1_r = 2 * curr_y + 1
                p1_c = 2 * curr_x + 1
                p2_r = 2 * next_y + 1
                p2_c = 2 * next_x + 1

                solve_pixels.add((p2_r, p2_c))
                mid_r = (p1_r + p2_r) // 2
                mid_c = (p1_c + p2_c) // 2
                solve_pixels.add((mid_r, mid_c))
                curr_y, curr_x = next_y, next_x
        for r in range(canvas_h):
            line = ""
            for c in range(canvas_w):
                is_wall = matrix[r][c] == 1
                is_42 = matrix[r][c] == 2
                is_entry = (r == entry[1] * 2 + 1 and c == entry[0] * 2 + 1)
                is_exit = (
                    r == exit_node[1] * 2 + 1 and c == exit_node[0] * 2 + 1)
                if fla % 2:
                    is_solve = (r, c) in solve_pixels
                if is_wall:
                    line += f"{self.WALL_COLOR}  {self.RESET}"
                elif is_entry:
                    line += f"{self.START_COLOR}🚕{self.RESET}"
                elif is_exit:
                    line += f"🏁{self.RESET}"
                elif is_42:
                    line += f"{self.FORTY2_COLOR}  {self.RESET}"
                elif fla % 2 and is_solve:
                    line += f"{self.SOLVE_COLOR}  {self.RESET}"
                else:
                    line += f"{self.PATH_COLOR}  {self.RESET}"
            output.append(line)
        return output

    def create_solve_cor(
            self, entry: tuple[Any, Any], str: str) -> list[tuple[Any, Any]]:
        """Converts a string of directions into a list of coordinates
        representing the solution path.

        Args:
            entry (Tuple[int, int]): Starting coordinates.
            str (str): String of directions ('N', 'S', 'E', 'W').

        Returns:
            List[Tuple[int, int]]: List of coordinates
            traversed following the directions.
        """
        x, y = entry
        mylist = []
        for i in str:
            if i == 'S':
                y += 1
                mylist.append((y, x))
            if i == 'N':
                y -= 1
                mylist.append((y, x))
            if i == 'W':
                x -= 1
                mylist.append((y, x))
            if i == 'E':
                x += 1
                mylist.append((y, x))
        return mylist
