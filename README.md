<div align="center">

<img src="icon.png" width="200" alt="Minesweeper AI Logo"/>

# 🎮 Minesweeper AI

A Python-based Minesweeper game application with AI assistance to help players solve the puzzle.

</div>

---

## ✨ Features

### 🎯 Classic Minesweeper Game
- **3 difficulty levels**: Easy (9x9, 10 mines), Medium (16x16, 40 mines), Hard (30x16, 99 mines)
- **Graphical interface**: Built with Pygame featuring an attractive UI
- **Timer**: Game time tracking
- **Mine counter**: Display remaining mine count
- **Flag marking**: Mark suspicious cells with flags

### 🤖 Intelligent AI Assistant
- **AI Helper**: AI mode that can suggest optimal moves
- **Logic algorithms**: AI uses logical rules for inference
- **Auto detection**: AI can automatically detect safe cells and mine cells
- **2 game modes**: Player (manual play) and AI (AI assistance)

## 🚀 Installation and Setup

### System Requirements
- Python 3.13.7+ (tested with Python 3.13.7)
- Pygame 2.6.1

### Installation and Running

#### 1. Clone the repository
```bash
git clone https://github.com/GuenNhatKing/Minesweeper-play-with-AI.git
cd Minesweeper-play-with-AI
```

#### 2. Create virtual environment (recommended)
```bash
# Create virtual environment
python -m venv minesweeper-env

# Activate virtual environment
# Windows:
minesweeper-env\Scripts\activate
# macOS/Linux:
source minesweeper-env/bin/activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Run the application
```bash
python game.py
```

#### 5. Deactivate virtual environment (when done)
```bash
deactivate
```

## 🎮 How to Play

### 1. Select Difficulty
- **Easy**: 9x9 with 10 mines - Perfect for beginners
- **Medium**: 16x16 with 40 mines - Intermediate challenge
- **Hard**: 30x16 with 99 mines - Expert level challenge

### 2. Select Game Mode
- **Player**: Manual play without assistance
- **AI**: AI will provide suggestions and assistance during gameplay

### 3. Controls
- **Left click**: Reveal cell
- **Right click**: Flag/unflag cell
- **Smiley button**: 
  - Left click: Reset current game
  - Right click: Return to level selection

## 🧠 AI Algorithm

The AI uses 4 logical rules to reason and provide suggestions:

### Rule 1: All Neighbors Safe
**Rule**: If the number of a cell equals the count of flagged neighbors, all unprobed neighbors can be safely revealed.

**Example**:
```
? ? ?      . . .
? 3 ?  =>  . 3 .
! ! !      ! ! !
```
- `?` = unprobed cell (unknown if mine or not)
- `!` = flagged cell (known to have mine)  
- `.` = probed cell (known to have no mine)

Cell with number 3 has 3 flags around it, so remaining `?` cells are all safe.

### Rule 2: All Neighbors Mines
**Rule**: If the number of a cell equals the count of unprobed and flagged neighbors, all unprobed neighbors are mines.

**Example**:
```
. ? ?      . ! !
. 4 ?  =>  . 4 !
. 2 !      . 2 !
```
Cell with number 4 needs 4 mines, has 1 flag + 3 unprobed = 4, so all 3 unprobed cells are mines.

### Rule 3: Advanced Probing
**Rule**: Consider two number cells A and B. If A equals B minus the count of B's unprobed and flagged neighbors that are not A's neighbors, then all A's unprobed neighbors that are not B's neighbors are safe.

**Example**:
```
? ? ?        . . .
? 1 ? ?  =>  . 1 ? ?
? ? 4 .      . ? 4 .
  ? . !        ? . !
```
- A = cell with number 1, B = cell with number 4
- B has 3 cells (1 flag + 2 unprobed) that are not A's neighbors
- Since A = B - 3 (1 = 4 - 3), A's unprobed neighbors not adjacent to B are safe

### Rule 4: Advanced Flagging
**Rule**: Consider two number cells A and B. If B equals A minus the count of A's unprobed and flagged neighbors that are not B's neighbors, then all A's unprobed neighbors that are not B's neighbors are mines.

**Example**:
```
? ? ? ?      ! ? ? ?
? 3 1 2  =>  ! 3 1 2
    2 2 . .      2 2 . .
```
- A = cell with number 3, B = cell with number 1  
- A has 2 unprobed cells that are not B's neighbors
- Since B = A - 2 (1 = 3 - 2), A's unprobed neighbors not adjacent to B are mines

## 📁 Project Structure

```
minesweeper-ai/
├── game.py          # Main file, game launcher
├── core.py          # Core game logic, state management
├── ai.py            # AI algorithms and inference logic
├── ui.py            # User interface and rendering
├── config.py        # UI and game configuration constants
├── levels.py        # Game level definitions
├── timer.py         # Game timer handling
├── requirements.txt # Python dependencies
├── assets/          # Game assets
│   ├── fonts/       # Font files
│   └── icons/       # Game icons
└── README.md        # This file
```

## 🛠️ Main Modules

### `core.py`
- Game state management
- Basic minesweeper logic
- Game board and cell management

### `ai.py`
- AI helper algorithms
- Logical inference rules
- Automatic suggestion generation

### `ui.py`
- Game interface rendering
- User input handling
- Game state display

### `game.py`
- Main game loop
- Module integration
- Event handling

## 🤝 Contributing

All contributions are welcome! Please create issues or pull requests.

## 🌟 Acknowledgments

This project was inspired by the concept of "semi-automatic minesweeper" from **Yusuke Endoh**'s brilliant implementation in the [International Obfuscated C Code Contest (IOCCC) 2020](https://www.ioccc.org/2020/endoh1/index.html). The core idea demonstrates that Minesweeper is not just about luck, but can be solved through logical inference.

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="right">

*Minesweeper AI - Half logic, half luck!*

</div>
