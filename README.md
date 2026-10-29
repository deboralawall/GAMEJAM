# Aquatic Memory Game

A small desktop memory game built with Python and Pygame. Match illustrated card pairs, race against the timer, and earn up to three stars based on your completion time. The game also includes a main menu, an instructions screen, and a story screen.

## Gameplay

- Choose a difficulty: Easy uses 2 pairs, Medium uses 3 pairs, and Hard uses 4 pairs.
- Click two cards to reveal them. Matching cards stay visible; non-matching cards are hidden again after a short delay.
- The game tracks elapsed time and turns. Matching all pairs displays a star rating: 3 stars for up to 20 seconds, 2 for up to 40 seconds, 1 for up to 60 seconds, and 0 after that.
- After a completed round, another round starts automatically at the same difficulty.

## Requirements

- Python
- Pygame

Install Pygame with pip:

```bash
python -m pip install pygame
```

## Run

From the project directory, start the main menu with:

```bash
python telaInicial.py
```

Keep the `imagens/` and `sons/` directories alongside the Python files; the game loads its graphics and sound effects from these folders.

## Project Structure

- `telaInicial.py` - main menu and navigation
- `choose_difficulty.py` - difficulty selection and game launch
- `jogodamemoria.py` - card matching, timer, turns, and score display
- `instructions.py` - instructions screen
- `historia.py` - story screen
- `imagens/` - card art, backgrounds, and star graphic
- `sons/` - sound effects
- `telaInicial.exe` - included executable build
