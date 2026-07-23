# Python EU4 Simulator

## About

A Python strategy game simulator inspired by Europa Universalis IV.

The project started as a beginner terminal script and grew into a GUI-based strategy simulator with countries, economy, recruitment, events, battles, automated tests, Git version control, and SQLite save slots.

## Current Features

- Tkinter GUI
- Start menu with New Game and Load Game
- Data-driven country selection that creates one button per loaded country
- Advisor selection with monthly advisor costs
- Monthly economy simulation
- Army maintenance
- Troop recruitment through the GUI
- Loans, interest, and bankruptcy logic
- Random event system with choice consequences
- Battle damage calculations
- Clickable map screen with country regions
- Map-based battle launching and battle result popup
- Country and map setup loaded from `countries.json`
- Pause menu with save/load/exit options
- SQLite save/load system with multiple save slots
- Dynamic load screen that creates one button per save
- Duplicate save names are automatically renamed with `_2`, `_3`, etc.
- Save slots can be deleted from the GUI
- Automated tests with `unittest`
- GitHub Actions workflow that automatically runs tests on GitHub
- Ruff static analysis for code quality checks
- Mypy static type checking across the active Python modules
- Dynamic country reports that support any number of loaded countries
- Data-driven country setup so new countries can be added by editing configuration data
- Rule-based AI decision prototype for recruit, attack, and wait actions
- Scrollable in-game world-events panel with live event history
- Structured world events for player recruitment, loans, AI recruitment, and AI attacks
- SQLite persistence for world-event history across save/load sessions

## Engineering Highlights

- Modular Python project split across backend systems, GUI coordinator code, and focused GUI helper modules
- Country and map startup data is loaded through a dedicated loader instead of being hardcoded in `main.py`
- `countries.json` separates gameplay stats from map drawing data
- Startup data validation catches missing country/map configuration before the GUI launches
- GUI helper package for save/load, recruitment, events, and advisor selection screens
- SQLite persistence layer with save slots, country rows, duplicate save-name handling, load support, and delete support
- Backend/game logic is tested separately from the Tkinter GUI
- Country-data tests use isolated temporary JSON files instead of modifying the real configuration
- Loader tests cover valid data, missing required fields, and mismatched country/map entries
- AI decisions use a typed dataclass so actions can carry targets and recruitment amounts
- AI behavior tests cover recruitment, target selection, waiting, and empty target lists
- World events use a typed `GameEvent` dataclass instead of unstructured GUI-only messages
- The world-events panel reads the current game log through a callback, so it keeps using the active game after a save is loaded
- Save/load tests verify that structured world events survive a SQLite round trip and are deleted with their save slot
- Economy and AI tests verify generated event categories and acting countries
- `Country` uses a dataclass with `__post_init__` for setup logic such as discipline conversion and army costs
- GitHub Actions CI runs the automated test suite after pushes and pull requests
- Ruff checks the active project code for unused imports, unused variables, and common Python style issues
- Mypy checks annotated and unannotated method bodies for incompatible types and missing attributes
- Event consequence dictionaries use `TypedDict` to document and verify their nested structure
- GUI helper classes construct their own widgets during initialization, reducing invalid setup states
- Country displays are generated from the country collection instead of fixed list indexes
- A project-local virtual environment isolates development tools from global Python packages
- Legacy JSON save files were replaced by the SQLite save system
- README, Git history, and GitHub repo are maintained as part of the project workflow

## Project Structure

- `main.py` - starts the GUI application
- `gui_app.py` - main GUI coordinator and shared Tkinter navigation
- `gui_helpers/` - focused GUI helper modules for save/load, recruitment, events, and advisors
- `game.py` - core game state and month progression
- `country.py` - dataclass for country stats, economy, loans, recruitment, and damage
- `country_data_loader.py` - loads and validates country/map setup data from JSON
- `countries.json` - data-driven country stats and map region configuration
- `battle.py` - battle resolution logic
- `ai_controller.py` - AI decision data and rule-based action selection
- `game_event.py` - structured records for world activity such as loans, recruitment, and attacks
- `map_ui.py` - clickable Tkinter canvas map and battle result popup
- `event_system.py` - random events and their effects
- `save_repository.py` - SQLite save/load/delete system
- `test_game.py` - automated tests
- `pyproject.toml` - Ruff and mypy configuration for static code checks
- `.github/workflows/tests.yml` - GitHub Actions workflow that runs tests after pushes and pull requests

## Running the Game

Run the GUI version:

```powershell
python main.py
```

## Development Environment

Create and activate the project virtual environment on Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install ruff mypy
```

The generated `.venv/` directory is ignored by Git.

## Running the Tests

```powershell
python -m unittest -v
```

GitHub Actions also runs the test suite automatically when code is pushed to GitHub.

## Running Code Quality Checks

```powershell
python -m ruff check .
python -m mypy .
```

Ruff checks the active project code for unused imports, unused variables, and common Python style issues. Mypy checks type annotations and method bodies across the active modules. The legacy folder is excluded from both tools.

## Save System

The save system uses SQLite through `save_repository.py`.

The database stores:

- save slot name
- current month
- selected player country
- monthly advisor expenses
- country stats for each saved country
- structured world-event history

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
- Continue expanding data-driven country/map configuration
- Continue separating GUI code from backend game logic
- Continue splitting large GUI sections into focused UI modules
- Polish the GUI layout and user feedback
- Expand the map system beyond the first prototype regions

## What I Learned

This project helped me learn:

- Classes, objects, `self`, and `__init__`
- Dataclasses and `__post_init__`
- Splitting a program into multiple modules
- GUI programming with Tkinter
- Buttons, frames, labels, entries, callbacks, and dynamic widgets
- Tkinter Canvas basics for drawing clickable map regions
- Tkinter popup windows with `Toplevel`
- JSON saving and loading
- Data-driven configuration with JSON
- Validating configuration data before the app starts
- SQLite databases
- SQL tables, rows, primary keys, foreign keys, `SELECT`, `INSERT`, `UPDATE`, and `DELETE`
- Turning database rows back into Python objects
- Input validation and exception handling
- Automated tests with `unittest`
- Testing expected exceptions with `assertRaises`
- Creating and automatically cleaning up temporary test files
- Static analysis and linting with Ruff
- Static type checking with mypy
- Type hints including unions, callbacks, `TypedDict`, class-level annotations, and `cast`
- Returning and testing lists of structured event objects across backend systems
- Building a scrollable Tkinter text panel and toggling it with callbacks
- Virtual environments for isolated project dependencies
- Designing collection-based displays without fixed list indexes
- Separating user interface code from backend logic
- Git and GitHub version control
- GitHub Actions for automatic test runs
