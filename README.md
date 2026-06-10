# Python EU4 Simulator

## About

A terminal-based strategy game simulator inspired by Europa Universalis IV.

## Features

- Multiple playable countries
- Monthly economy and army maintenance
- Advisors and income
- Loans, interest, and bankruptcy
- Troop recruitment
- Battle calculations
- Random events with multiple choices
- JSON save and load system
- Automated tests

## Project Structure

- `test_main.py` - starts the game
- `game.py` - game loop, saving, loading, and advisors
- `country.py` - country economy, troops, loans, and damage
- `battle.py` - battle calculations
- `event_system.py` - random events and their effects
- `test_game.py` - automated tests

## Running the Game

```powershell
python test_main.py
```

## Running the Tests

```powershell
python -m unittest -v
```

## What I Learned

This project helped me learn:

- Classes, objects, `self`, and `__init__`
- Splitting a program into multiple modules
- JSON saving and loading
- Input validation and exception handling
- Automated tests with `unittest`
- Separating user input from game logic
- Git version control