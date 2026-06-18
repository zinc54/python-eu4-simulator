# Python EU4 Simulator

## About

A Python strategy game simulator inspired by Europa Universalis IV.

The project started as a beginner terminal script and grew into a GUI-based strategy simulator with countries, economy, recruitment, events, battles, automated tests, Git version control, and SQLite save slots.

## Current Features

- Tkinter GUI
- Start menu with New Game and Load Game
- Country selection
- Advisor selection with monthly advisor costs
- Monthly economy simulation
- Army maintenance
- Troop recruitment through the GUI
- Loans, interest, and bankruptcy logic
- Random event system with choice consequences
- Battle damage calculations
- Pause menu with save/load/exit options
- SQLite save/load system with multiple save slots
- Dynamic load screen that creates one button per save
- Duplicate save names are automatically renamed with `_2`, `_3`, etc.
- Save slots can be deleted from the GUI
- Automated tests with `unittest`

## Project Structure

- `main.py` - starts the GUI application
- `gui_app.py` - main GUI application and Tkinter screens
- `game.py` - core game state and month progression
- `country.py` - dataclass for country stats, economy, loans, recruitment, and damage
- `battle.py` - battle resolution logic
- `event_system.py` - random events and their effects
- `save_repository.py` - SQLite save/load/delete system
- `test_game.py` - automated tests

## Running the Game

Run the GUI version:

```powershell
python main.py
```

## Running the Tests

```powershell
python -m unittest -v
```

## Save System

The save system uses SQLite through `save_repository.py`.

The database stores:

- save slot name
- current month
- selected player country
- monthly advisor expenses
- country stats for each saved country

The GUI can:

- create named save slots
- automatically rename duplicate save names with `_2`, `_3`, etc.
- list existing saves
- load a selected save
- delete saves from the database
- handle the first-time-player case where no saves exist yet

## Notes

The current main version is the GUI + SQLite version.

Future cleanup goals:

- Add stronger save-name validation
- Continue separating GUI code from backend game logic
- Split large GUI sections into smaller modules when the boundaries are clear
- Polish the GUI layout and user feedback

## What I Learned

This project helped me learn:

- Classes, objects, `self`, and `__init__`
- Dataclasses and `__post_init__`
- Splitting a program into multiple modules
- GUI programming with Tkinter
- Buttons, frames, labels, entries, callbacks, and dynamic widgets
- JSON saving and loading
- SQLite databases
- SQL tables, rows, primary keys, foreign keys, `SELECT`, `INSERT`, `UPDATE`, and `DELETE`
- Turning database rows back into Python objects
- Input validation and exception handling
- Automated tests with `unittest`
- Separating user interface code from backend logic
- Git and GitHub version control
