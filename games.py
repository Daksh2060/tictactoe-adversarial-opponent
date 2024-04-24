"""Games or Adversarial Search (Chapter 5)"""

import copy
import itertools
import random
from collections import namedtuple

import numpy as np

#from utils import vector_add

GameState = namedtuple('GameState', 'to_move, utility, board, moves')

def gen_state(to_move='X', x_positions=[], o_positions=[], h=3, v=3):
    """Given whose turn it is to move, the positions of X's on the board, the
    positions of O's on the board, and, (optionally) number of rows, columns
    and how many consecutive X's or O's required to win, return the corresponding
    game state"""

    moves = set([(x, y) for x in range(1, h + 1) for y in range(1, v + 1)]) - set(x_positions) - set(o_positions)
    moves = list(moves)
    board = {}
    for pos in x_positions:
        board[pos] = 'X'
    for pos in o_positions:
        board[pos] = 'O'
    return GameState(to_move=to_move, utility=0, board=board, moves=moves)


# ______________________________________________________________________________
# MinMax Search

# Regular minmax, came provided with template file, left unchanged
def minmax(game, state):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""
    print("minmax working")
    player = game.to_move(state)

    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a)))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a)))
        return v

    # Body of minmax_decision:
    return max(game.actions(state), key=lambda a: min_value(game.result(state, a)))


# minmax cutoff, is the same as the regular version, but uses a custom cutoff test and evluation function
# as suggested by the textbook:
# unwinnable at cutoff depth of 3 or greater, while very hard to beat at 2
def minmax_cutoff(game, state, cutoff_depth):
    print("minmax_cutoff working")
    player = game.to_move(state)

    def max_value(state, depth):
        if game.terminal_test(state) or depth == cutoff_depth: #used my own cutoff test
            return game.evaluation_func(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), depth + 1))
        return v

    def min_value(state, depth):
        if game.terminal_test(state) or depth == cutoff_depth: #used my own cutoff test
            return game.evaluation_func(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), depth + 1))
        return v

    return max(game.actions(state), key=lambda a: min_value(game.result(state, a), 1))

    print("minmax_cutoff: to be done by studens")
    return None

# ______________________________________________________________________________

# expect minmax implemented as suggest by textbook figure 5.11 with a few adjustments
# chances node has been modified to assume each state is equally likely
def expect_minmax(game, state):
    """
    [Figure 5.11]
    Return the best move for a player after dice are thrown. The game tree
	includes chance nodes along with min and max nodes.
	"""
    print("expect_minmax working")
    player = game.to_move(state)

    def max_value(state):
        v = -np.inf
        for a in game.actions(state):
            v = max(v, chance_node(state, a))
        return v

    def min_value(state):
        v = np.inf
        for a in game.actions(state):
            v = min(v, chance_node(state, a))
        return v

    def chance_node(state, action):     
        res_state = game.result(state, action)  
        if game.terminal_test(res_state):
            return game.utility(res_state, player)
        sum_chances = 0
        num_chances = len(game.chances(res_state)) #Chances returns a list of all possible game states
        for chance in game.chances(res_state):
            util = 0
            if chance.to_move == player: #return max score for maximizing agent(player)
                util = max_value(chance) #return min score for minimzing agent(bot)
            else:
                util = min_value(chance)
            sum_chances += util #assuming every state is equally possible, we use the average utility
        return sum_chances / num_chances

    # Body of expect_minmax:
    return max(game.actions(state), key=lambda a: chance_node(state, a))
    print("chance_node: to be completed by students")



# expect minmax with cutoff uses the cutoff test and evaluation function
# works as expected but is not unbeatable due to averaging of utility, which
# works against the evalution function, should be smarter with higher depths
def expect_minmax_cutoff(game, state, cutoff_depth):
    print("expect_minmax_cutoff working")
    player = game.to_move(state)

    def max_value(state, depth):
        if game.cutoff_test(state, depth):
            return game.evaluation_func(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, chance_node(state, a, depth + 1))
        return v

    def min_value(state, depth):
        if game.cutoff_test(state, depth):
            return game.evaluation_func(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, chance_node(state, a, depth + 1))
        return v

    def chance_node(state, action, depth):
        res_state = game.result(state, action)
        if game.cutoff_test(state, depth):
            return game.evaluation_func(state, player)
        sum_chances = 0
        num_chances = len(game.chances(res_state)) #Chances returns a list of all possible game states
        for chance in game.chances(res_state):
            util = 0
            if chance.to_move == player: #return max score for maximizing agent(player)
                util = max_value(chance) #return min score for minimzing agent(bot)
            else:
                util = min_value(chance)
            sum_chances += util #assuming every state is equally possible, we use the average utility
        return sum_chances / num_chances

    return max(game.actions(state), key=lambda a: chance_node(state, a, 1))
    print("expect_minmax_cutoff working")


# alpha beta also implemented according to the textbook outline, no major changes
# should be unwinnable at smaller sizes, unsure about larger due to runtime
def alpha_beta_search(game, state):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    print("alpha_beta_search working")
    player = game.to_move(state)

    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v
    
    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    best_score = -np.inf
    beta = np.inf
    chosen_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta)
        if v > best_score:
            best_score = v
            chosen_action = a
    return chosen_action
    print("alpha_beta_search: to be completed by students")
    

# similarly to minmax, only the cutoff test and evalution function are switched in
# unwinnable at cutoff depth of 3 or greater, while very hard to beat at 2
def alpha_beta_cutoff_search(game, state, cutoff_depth):
    print("alpha_beta_cutoff_search working")
    player = game.to_move(state)

    def max_value(state, alpha, beta, depth):
        if game.terminal_test(state) or depth == cutoff_depth: #used my own cutoff test
            return game.evaluation_func(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if game.terminal_test(state) or depth == cutoff_depth: #used my own cutoff test
            return game.evaluation_func(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    best_score = -np.inf
    beta = np.inf
    chosen_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            chosen_action = a
    return chosen_action

    print("alpha_beta_cutoff_search: may be used, if so, must be implemented by students")
    


# ______________________________________________________________________________
# Players for Games


def query_player(game, state):
    """Make a move by querying standard input."""
    print("current state:")
    game.display(state)
    print("available moves: {}".format(game.actions(state)))
    print("")
    move = None
    if game.actions(state):
        move_string = input('Your move? ')
        try:
            move = eval(move_string)
        except NameError:
            move = move_string
    else:
        print('no legal moves: passing turn to next player')
    return move


# Removed template function calls to directly pass depth manually
def random_player(game, state):
    """A player that chooses a legal move at random."""
    return random.choice(game.actions(state)) if game.actions(state) else None


# ______________________________________________________________________________
# 


class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))



class TicTacToe(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to_move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'.
    depth = -1 means max search tree depth to be used."""

    def __init__(self, h=3, v=3, k=3, d=-1):
        self.h = h
        self.v = v
        self.k = k
        self.depth = d
        moves = [(x, y) for x in range(1, h + 1)
                 for y in range(1, v + 1)]
        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)

    def actions(self, state):
        """Legal moves are any square not yet taken."""
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((x, y), '.'), end=' ')
            print()

    def compute_utility(self, board, move, player):
        """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        if (self.k_in_row(board, move, player, (0, 1)) or
                self.k_in_row(board, move, player, (1, 0)) or
                self.k_in_row(board, move, player, (1, -1)) or
                self.k_in_row(board, move, player, (1, 1))):
            return self.k if player == 'X' else -self.k
        else:
            return 0

    # As per the guideline from in lecture, eval function returns the difference in scores of
    # player and opponent on the current state, should be unbeatable when used since it causes
    # bot agent to focus on preventing player win.
    def evaluation_func(self, state, player):
        
        if self.terminal_test(state):
            return self.utility(state, player)

        player_score = 0
        opponent_score = 0

        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                if state.board.get((x, y)) == player:
                    player_score += 1
                elif state.board.get((x, y)) == ('X' if player == 'O' else 'O'):
                    opponent_score += 1

        return player_score - opponent_score
        print("evaluation_function: to be completed by students")
		
    def k_in_row(self, board, move, player, delta_x_y):
        """Return true if there is a line through move on board for player.
        hint: This function can be extended to test of n number of items on a line 
        not just self.k items as it is now. """
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n >= self.k

    
    def cutoff_test(self, state, depth):
        """Determines whether to cutoff the search at a given depth."""
        # If depth limit is not reached or the state is terminal, don't cutoff
        return depth >= self.depth or self.terminal_test(state)

    # examines the current state and returns an array of the possible states following
    def chances(self, state):
        """Return a list of all possible states."""
        chances = []
        for move in self.actions(state):
            new_state = self.result(state, move)
            chances.append(new_state)
        return chances
    
class Gomoku(TicTacToe):
    """Also known as Five in a row."""

    def __init__(self, h=15, v=16, k=5):
        TicTacToe.__init__(self, h, v, k)
