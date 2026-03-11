import sys
# Assuming mazegen exists in the environment or same folder
try:
    from mazegen import MazeGenerator
except ImportError:
    # Mocking for standalone testing if file is missing
    print("Warning: generator module not found. Maze generation will fail.")
    class MazeGenerator:
        def __init__(self, w, h): pass
        def main_generator(self, p, o, c): pass

from display import Display
from parsing import Mazeconfig


def generate(ds: Display, check: int, param: dict) -> None:
    """Generates a maze, saves it to a file, and displays it."""
    try:
        m = MazeGenerator(param["WIDTH"], param["HEIGHT"])
        m.main_generator(param, param["OUTPUT_FILE"], check)
        
        arr = ds.read_hex(param["OUTPUT_FILE"])
        if arr:
            w = param["WIDTH"]
            h = param["HEIGHT"]
            result = ds.draw(
                arr, w, h, param["ENTRY"], param["EXIT"], 
                solve=[], fla=0
            )
            for row in result:
                print(row)
        else:
            print("Failed to read generated maze.")
    except Exception as e:
        print(f"Error in generation: {e}")


def solve_and_draw(ds: Display, flag: int, param: dict) -> None:
    """Reads the solution path and displays the maze with the path."""
    direction_str = ds.read_dir(param["OUTPUT_FILE"])
    if not direction_str:
        print("No solution found in file.")
        return

    cor = ds.create_solve_cor(param["ENTRY"], direction_str)
    matrice = ds.read_hex(param["OUTPUT_FILE"])
    
    if matrice:
        w = param["WIDTH"]
        h = param["HEIGHT"]
        result = ds.draw(
            matrice, w, h, param["ENTRY"], param["EXIT"], cor, flag
        )
        for row in result:
            print(row)


def menu(param: dict) -> None:
    """Displays the interactive menu for maze operations."""
    ds = Display()
    # Clear screen
    print('\x1B[2J\x1B[H', end='')
    
    # Generate initial maze
    try:
        generate(ds, 1, param)
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return
    
    flag = 1 # Flag controls visibility of path (odd=show, even=hide in logic)
    
    while True:
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")

        try:
            user_input = input("choice? (1-4):> ")
            if not user_input.strip():
                continue
            n = int(user_input)
            
            match n:
                case 1:
                    print('\x1B[2J\x1B[H', end='')
                    generate(ds, 0, param)
                    flag = 1 # Reset flag
                case 2:
                    print('\x1B[2J\x1B[H', end='')
                    # Increment flag to toggle odd/even logic in draw
                    solve_and_draw(ds, flag, param)
                    flag += 1
                case 3:
                    while True:
                        print("\nChoose your color for wall:")
                        print("1. Purple")
                        print("2. Green")
                        print("3. Blue")
                        print("4. Back")
                        try:
                            c_input = input("choice? (1-4):> ")
                            if not c_input.strip(): continue
                            c = int(c_input)
                            
                            if c == 1:
                                ds.WALL_COLOR = '\033[105m'
                                ds.FORTY2_COLOR = '\033[107m'
                                break
                            elif c == 2:
                                ds.WALL_COLOR = '\033[48;5;118m'
                                ds.FORTY2_COLOR = '\033[107m'
                                break
                            elif c == 3:
                                ds.WALL_COLOR = '\033[48;5;117m'
                                ds.FORTY2_COLOR = '\033[105m'
                                break
                            elif c == 4:
                                break
                            else:
                                print("Invalid color choice.")
                        except ValueError:
                            print("Please enter a valid number.")
                        except EOFError:
                            print("\nReturning to main menu...")
                            break
                    
                    # Redraw with new colors
                    print('\x1B[2J\x1B[H', end='')
                    solve_and_draw(ds, flag - 1 if flag > 1 else 0, param)

                case 4:
                    print("\nGoodbye!")
                    sys.exit()
                case _:
                    print("Invalid option.")
        except ValueError:
            print("Please enter a number.")
        except EOFError:
            print("\nExiting program (EOF detected).")
            sys.exit()
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user. Press 4 to quit or continue.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            raise Exception("Usage: python3 a_maze_ing.py <config_file>")
        
        if sys.argv[1]:
            config = Mazeconfig()
            param = config.load_config(sys.argv[1])
            
            if not param:
                print("Error: Failed to load configuration.")
                sys.exit(1)

            # Validate required keys
            required_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE"]
            missing_keys = [key for key in required_keys if key not in param]
            
            if missing_keys:
                print(f"Error: Missing configuration parameters: {', '.join(missing_keys)}")
                sys.exit(1)

            entry_x, entry_y = param["ENTRY"]
            exit_x, exit_y = param["EXIT"]
            w, h = param["WIDTH"], param["HEIGHT"]

            if (entry_x < 0 or entry_y < 0) or (entry_x >= w or entry_y >= h):
                raise Exception(f"Entry position {param['ENTRY']} is out of bounds (Size: {w}x{h})")
            if (exit_x < 0 or exit_y < 0) or (exit_x >= w or exit_y >= h):
                raise Exception(f"Exit position {param['EXIT']} is out of bounds (Size: {w}x{h})")
            if (entry_x == exit_x) and (entry_y == exit_y):
                raise Exception("Entry and exit cannot be the same coordinates.")
            
            menu(param)
    except Exception as e:
        print(f"Error: {e}")