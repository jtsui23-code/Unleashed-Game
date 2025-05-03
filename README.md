# 🎮 Unleashed - Turn-Based Roguelike (Python, Pygame)

## 📝 Description

**Unleashed** is a turn-based roguelike game developed in Python using Pygame, created by **Jack Tsui**, **Zachary Barrentine**, **Zach Lewis**, **Daniel Prince**, and **Gage Ahlmark**. Originally a small prototype, the game has evolved into a more substantial collaborative project with character progression, resource upgrades, and dynamic menu-driven battles.

---

## 🚀 Features

### ✅ Implemented
- Turn-based combat with enemy encounters
- Skill system and cooldown management
- Upgrade shop with coin-based economy
- Interactive dialogue system
- Inventory with usable items (e.g., potions)
- Multiple game states: main menu, shop, battle, game over
- Modular code structure using OOP principles

### 🔜 Work In Progress
- Procedural level generation
- Save/load functionality
- Smarter enemy behavior and basic AI logic
- Additional enemies and boss mechanics
- Sound effect integration and polish

---

## 📁 Project Structure

| #   | File / Directory | Description |
|-----|------------------|-------------|
| 1   | [Game.py](https://github.com/jtsui23-code/Unleashed-Game/blob/main/Game.py) | Main game loop and state manager |
| 2   | [`Scripts/character.py`](https://github.com/jtsui23-code/Unleashed-Game/blob/main/Scripts/character.py) | Character and skill class definitions |
| 3   | [`Scripts/enemies.py`](https://github.com/jtsui23-code/Unleashed-Game/blob/main/Scripts/enemies.py) | Enemy class implementations |
| 4   | [`Scripts/saveStates.py`](https://github.com/jtsui23-code/Unleashed-Game/blob/main/Scripts/saveStates.py) | Save/load system |
| 5   | [`Scripts/ui.py`](https://github.com/jtsui23-code/Unleashed-Game/blob/main/Scripts/ui.py) | Buttons, text boxes, and UI elements |
| 6   | [`Scripts/upgrade.py`](https://github.com/jtsui23-code/Unleashed-Game/blob/main/Scripts/upgrade.py) | Upgrade mechanics and UI bars |
| 7   | [`Scripts/util.py`](https://github.com/jtsui23-code/Unleashed-Game/blob/main/Scripts/util.py) | Asset loading and helper functions |
| 8   | [`Scripts/dialogue.py`](https://github.com/jtsui23-code/Unleashed-Game/blob/main/Scripts/dialogue.py) | Dialogue manager and text typing |
| 9   | [`Scripts/allDialogues.py`](https://github.com/jtsui23-code/Unleashed-Game/blob/main/Scripts/allDialogues.py) | Static dialogue strings |
| 10  | [`Media/`](https://github.com/jtsui23-code/Unleashed-Game/tree/main/Media) | Game assets: sprites, fonts, music |

---

## 🧠 What We’re Learning

- Game state management using object-oriented programming
- UI/UX design within a game engine framework (Pygame)
- Modular design and teamwork using GitHub
- Turn-based battle mechanics and logic flow
- Planning and iterating on game systems

---

## ▶️ How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/jtsui23-code/Unleashed-Game.git
   cd Unleashed-Game
   ```
2. Download Pygame:
   ```
   pip install pygame
   ```
3. Run the game:
   ```
   Python Game.py
   ```
