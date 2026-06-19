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
- GitHub Actions workflow that automatically runs tests on GitHub

## Engineering Highlights

- Modular Python project split across backend systems, GUI coordinator code, and focused GUI helper modules
- GUI helper package for save/load, recruitment, events, and advisor selection screens
- SQLite persistence layer with save slots, country rows, duplicate save-name handling, load support, and delete support
- Backend/game logic is tested separately from the Tkinter GUI
- `Country` uses a dataclass with `__post_init__` for setup logic such as discipline conversion and army costs
- GitHub Actions CI runs the automated test suite after pushes and pull requests
- Legacy JSON save files were replaced by the SQLite save system
- README, Git history, and GitHub repo are maintained as part of the project workflow

## Project Structure

- `main.py` - starts the GUI application
- `gui_app.py` - main GUI coordinator and shared Tkinter navigation
- `gui_helpers/` - focused GUI helper modules for save/load, recruitment, events, and advisors
- `game.py` - core game state and month progression
- `country.py` - dataclass for country stats, economy, loans, recruitment, and damage
- `battle.py` - battle resolution logic
- `event_system.py` - random events and their effects
- `save_repository.py` - SQLite save/load/delete system
- `test_game.py` - automated tests
- `.github/workflows/tests.yml` - GitHub Actions workflow that runs tests after pushes and pull requests

## Running the Game

Run the GUI version:

```powershell
python main.py
```

## Running the Tests

```powershell
python -m unittest -v
```

GitHub Actions also runs the test suite automatically when code is pushed to GitHub.

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
- Continue splitting large GUI sections into focused UI modules
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
- GitHub Actions for automatic test runs
