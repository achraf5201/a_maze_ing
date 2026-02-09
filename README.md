*This project has been created as part of the 42 curriculum by ael-bala, mbouskha*

# 🧩 A-Maze-ing — This is the way

## 📖 Description

**A-Maze-ing** is a maze generator written in **Python 3**.  
The program reads a configuration file, generates a random maze (perfect or not),
exports it using a hexadecimal wall representation, and provides a visual display
in the terminal.

This project explores:
- Maze generation algorithms
- Grid and graph logic
- Code modularity and reusability
- Configuration-driven programs
- Terminal visualization

---

## ⚙️ Instructions

### ▶️ Execution

```bash
python3 a_maze_ing.py config.txt
```
a_maze_ing.py is the main program.

config.txt is a plain text configuration file.

All errors (invalid config, file not found, impossible maze, etc.) are handled
gracefully with clear messages. The program must never crash unexpectedly.

### 🧾 Configuration File Format

The configuration file contains one KEY=VALUE per line.
Lines starting with # are ignored.
```
Mandatory keys:
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```
### 🧠 Maze Generation Algorithm

Chosen Algorithm: Depth-First Search (Recursive Backtracker)
The algorithm starts from a cell, randomly explores unvisited neighbours,
removes walls between connected cells, and continues recursively until all
cells are visited.

### Why this algorithm?

- Simple and efficient

- Produces perfect mazes naturally

- Low memory usage

- Easy to reproduce mazes using a random seed

- When PERFECT=True, the maze contains exactly one valid path between the entry
and the exit.

## 📚 Resources

- https://www.geeksforgeeks.org/dsa/depth-first-search-or-dfs-for-a-graph/

- Python official documentation

- Graph theory fundamentals

- Stack Overflow discussions

## AI usage

### AI tools were used to:

- Review algorithm concepts

- Improve documentation structure

- Clarify technical explanations

- All AI-generated content was reviewed, understood, and adapted manually.


## 👥 Team & Project Management

This project was developed by two team members with clearly defined roles.

- **ael-bala**
  - Maze solving and pathfinding
  - Configuration file parsing
  - Reusable module packaging (`mazegen-*`)
  - Error handling

- **mbouskha**
  - Maze generation using DFS
  - “42” pattern generation
  - Menu system and user interactions
  - Maze display and visualization

The project was developed incrementally with a focus on modularity,
clear responsibility separation, and robust error handling.
