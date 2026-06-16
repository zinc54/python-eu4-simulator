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
- Automated tests with `unittest`

## Project Structure

- `gui.py` - main GUI application and Tkinter screens
- `game.py` - core game state, month progression, legacy terminal/JSON logic
- `country.py` - country stats, economy, loans, recruitment, and damage
- `battle.py` - battle resolution logic
- `event_system.py` - random events and their effects
- `save_repository.py` - SQLite save/load system
- `test_game.py` - automated tests
- `test_main.py` - older terminal launcher kept for now as legacy code
- `save_game.json` / `test_save_game.json` - older JSON save files kept for compatibility/tests

## Running the Game

Run the GUI version:

```powershell
python gui.py
```

## Running the Tests

```powershell
python -m unittest -v
```

## Save System

The current save system uses SQLite through `save_repository.py`.

The database stores:

- save slot name
- current month
- selected player country
- monthly advisor expenses
- country stats for each saved country

The GUI can list saves from the database and load the selected save by its `save_id`.

## Notes

The project still contains older JSON and terminal code from earlier versions. The current main version is the GUI + SQLite version.

Future cleanup goals:

- Replace old JSON tests with SQLite repository tests
- Remove or archive the old terminal launcher
- Add empty-save handling for first-time players
- Add save name validation
- Prevent or rename duplicate save names
- Reduce debug printing from backend classes

## What I Learned

This project helped me learn:

- Classes, objects, `self`, and `__init__`
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
