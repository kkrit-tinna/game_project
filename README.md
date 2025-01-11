
# Memory Matching Game
Memory Match is a is a game (often using playing cards) that requires players to remember and match similar elements. 
If using cards, the player turns over two cards at a time and tries to match pairs in as few "moves" as possible.
This project reimagines the game process and replaces physical cards with its online counterparts.


## Description
* Players can input their names through a pop-up window, decide which card deck they can plau with (poker cards is the default), and select the number of cards to play with. 
  * The allowable options are 8, 10, and 12 cards.
* The main board displays cards for matching game, Consider the player entering their guess after they’ve selected a card and then tried to match it with another card selection.
  * It also displays a “status” area that presents the player with their current number of guesses and matches.
  * It also displays a “leader board” that keeps track of “top player” scores.

## Getting Started

### Dependencies

* This program can be run on Windows, MacOS, and Linux.
* Must install any IDE that can interpret **Python** files (Mine is VScode).
* Pre-req Python Libraries include: Turtle, random, time.

### Installing

* You can download this project via https://github.com/kkrit-tinna/game_project.git

### Executing program

* To begin, locate the Python file memory_game.py and run it. Once launched, you’re ready to enjoy an engaging memory match game!
```
from game import Game

def main():
    game = Game()
    game.play_game()
```
* This program is built using three classes: Game, Board, and Card.
* Game
  * Prompts players to enter their names and select the number of cards to play with.
  * Let players choose between two card decks: a standard poker deck or a set of adorable dog images (read from a configuration file).
  * Reads images from a configuration file and randomizes them before passing control to the class Board.

```
from turtle import Turtle, Screen, numinput
import random
import time
from board import Board
```

* Board
  * Manages all board-related activities.
  * Creates the game layout, places randomized cards on the board, and updates the leaderboard.
  * Tracks gameplay progress by monitoring guesses and matches in each round.
  * Handles clicks by introducing actions in class Card until all matches are complete, or the player exiting the game.

```
from turtle import Turtle, Screen
from card import Card
```

* Card
  * Manages card-specific actions.
  * Flips cards, checks if two cards match, and restores unmatched cards to their original states.


## Author
Yifei Shi


## Version History
* 0.1
    * Initial Release
