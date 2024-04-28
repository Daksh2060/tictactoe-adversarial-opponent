# Tic-Tac-Toe Adversarial Agent

This is a project template from UC Berkeley, for an adversarial agent. This specific implementation is for playing Tic Tac Toe, offering users the option to choose board size and difficulty level. The agent utilizes various search algorithms including, but not limited to; Alpha-Beta Pruning, Expectimax, and Minimax. Each algorithm is implemented both with and without cutoff distances to allow users to experiment with different strategies and observe their impact on gameplay. The project provides an interactive interface where users can play against the adversarial agent, selecting the board size and difficulty level according to their preference. 

## Features

- **Selectable Board Size:** Games can be played at any selecatble n x n board size. Note; larger boards with certain algorithms may run slower during testinng.

- **Selectable Difficulty:** Utilize simiplier/more advanced search algorithms or lower/higher cutoff depths to lower/raise the difficulty,

- **Unwinnable difficulty:** The games becomes very difficult / unwinnable at certain difficltiuies, utilizing cutoff depth and evalution functions to adjust adverisal bot optimizition.

## How does it work?

Using a tkinter UI to display the game state, users can select the aglorithm utilized by the adversial agent, as well as the cutoff depth, creating an adjustable diffilcituly. The game is unwinnable with past cetain cutoff depths as the evalutation fnction can optimially decide how to block users from winning, it is however every rare for the adversail bbot to win, with draws being the most likely outcome. Large cutoff depths in conjunction with large board zies may lead to performance issues due to this.

<p align="center">
  <img src="" />
</p>

## Algorithms

- **Alpha-Beta Pruning**

- **Expectimax:**

- **Minimax:**

## Requirements

- Python 3.x

- Modules: `numpy`

## Installation and Use

Follow these steps to set up and run the Tic-Tac-Toe game:

1. Download or clone the repository to your local machine:

  ```bash
  git clone https://github.com/Daksh2060/tictactoe-adversarial-opponent
  ```

2. Install `numpy` and `pygame` if not already installed:

  - **numpy:** [Install numpy with pip](https://numpy.org/install/)

  - **pip:** [Install pip (usually included with python)](https://pip.pypa.io/en/stable/installation/)

3. Run `tic-tac-toe.py` to start the game.

4. To specifcy board size, follow launch command with the following:

  ```bash
  C:/Users/.../python.exe c:/Users/.../tictactoe-adversarial-opponent/tic-tac-toe.py 3 3 3
  ```
  This will result in a 3 x 3 game board, if left blank will default to a 5 x 5.

5. Adjust difficult by choosing a search algorithm, and if using a cutoff variant, adjust the cutoff distance.
   
## Contact

Feel free to reach out if you have any questions, suggestions, or feedback:

- **Email:** dpa45@sfu.ca
- **LinkedIn:** [@Daksh Patel](https://www.linkedin.com/in/daksh-patel-956622290/)

