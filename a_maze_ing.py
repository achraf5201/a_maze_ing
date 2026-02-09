import sys
from mazegen import MazeGenerator
from src import display, Mazeconfig


def generate(ds: display, check: int, param: dict) -> None:
    """Generates a maze, saves it to a file, and displays it.

    Args:
        ds (display): Display object used for rendering.
        check (int): Random seed flag; 1 for reproducible maze.
        param (dict): Maze parameters including
        WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE.
    """
    m = MazeGenerator(param["WIDTH"], param["HEIGHT"])
    m.main_generator(param, param["OUTPUT_FILE"], check)
    arr = ds.read_hex(param["OUTPUT_FILE"])
    if arr:
        w = param["WIDTH"]
        h = param["HEIGHT"]
        result = ds.draw(
            arr, w, h, param["ENTRY"], param["EXIT"], param["ENTRY"][0],
            param["ENTRY"][1])
        for row in result:
            print(row)


def solve_and_draw(ds: display, flag: int, param: dict) -> None:
    """Reads the solution path and displays the maze with the path.

    Args:
        ds (display): Display object used for rendering.
        flag (int): Toggle for showing/hiding path.
        param (dict): Maze parameters including
        WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE.
    """
    dir = ds.read_dir(param["OUTPUT_FILE"])
    cor = ds.create_solve_cor(param["ENTRY"], dir)
    matrice = ds.read_hex(param["OUTPUT_FILE"])
    if matrice:
        w = param["WIDTH"]
        h = param["HEIGHT"]
        result = ds.draw(
                matrice, w, h, param["ENTRY"], param["EXIT"], cor, flag)
        for row in result:
            print(row)


def menu(param: dict) -> None:
    """Displays the interactive menu for maze operations.

    Options include:
        1. Re-generate the maze
        2. Show/Hide solution path
        3. Rotate wall colors
        4. Quit

    Args:
        param (dict): Maze parameters including
        WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE.
    """
    ds = display()
    print('\x1B[2J\x1B[H', end='')
    generate(ds, 1, param)
    flag = 1
    while True:
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")

        try:
            n = int(input("choice? (1-4):> "))
            match n:
                case 1:
                    print('\x1B[2J\x1B[H', end='')
                    generate(ds, 0, param)
                    flag = 1
                case 2:
                    print('\x1B[2J\x1B[H', end='')
                    solve_and_draw(ds, flag, param)
                    flag += 1
                case 3:
                    print("choose your color for wall")
                    print("1. Purple")
                    print("2. green")
                    print("3. Blue")
                    print("4. back")
                    c = int(input("choice? (1-4):> "))
                    match c:
                        case 1:
                            ds.WALL_COLOR = '\033[105m'
                            ds.FORTY2_COLOR = '\033[107m'
                        case 2:
                            ds.WALL_COLOR = '\033[48;5;118m'
                            ds.FORTY2_COLOR = '\033[107m'
                        case 3:
                            ds.WALL_COLOR = '\033[48;5;117m'
                            ds.FORTY2_COLOR = '\033[105m'
                        case 4:
                            pass
                case 4:
                    sys.exit()
                case _:
                    print("Invalid option.")
        except ValueError:
            print("Please enter a number.")


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            raise Exception("You did not enter a file name")
        if sys.argv[1]:
            config = Mazeconfig()
            param = config.load_config(sys.argv[1])
            entry_x, entry_y = param["ENTRY"][0], param["ENTRY"][1]
            exit_x, exit_y = param["EXIT"][0], param["EXIT"][1]
            w, h = param["WIDTH"], param["HEIGHT"]
            if (entry_x < 0 or entry_y < 0) or (entry_x >= w or entry_y >= h):
                raise Exception("Entry position is invalid ")
            if (exit_x < 0 or exit_y < 0) or (exit_x >= w or exit_y >= h):
                raise Exception("exit position is invalid ")
            if (entry_x == exit_x) and (entry_y == exit_y):
                raise Exception("Entry and exit cannot be the same.")
            menu(param)
    except Exception as e:
        print(e)
