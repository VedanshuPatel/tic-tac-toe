# tic-tac-toe

Play classic 3×3 Tic-Tac-Toe in the terminal. You can challenge a friend locally or face the AI on Easy or Hard mode. X moves first, and each turn is a row and column numbered from 1 to 3 (such as `3 1`).


## Setup

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

## Run the game

    python3 main.py

Choose **1** for two human players or **2** for versus AI, then Easy or Hard if you play the AI. You are X, the AI is O.

## Run the tests

    pytest

Or with more detail:

    pytest -v