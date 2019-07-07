from collections import defaultdict
from math import *
import random
MAX_CHIPS = 3

class NimState:
    def __init__(self, ch):
        # Start out with player 1, the next player to move
        self.player = 1
        self.chips = ch

    def clone(self):
        cl = NimState(self.chips)
        cl.player = self.player
        return cl

    def doMove(self, move):
        if not 0 < move <= MAX_CHIPS:
            raise ValueError("The amount of chips taken per move must be between 0 and " + str(MAX_CHIPS))
        self.chips -= move

        # Switching between player 1 and 2
        self.player = 3 - self.player

    def getMoves(self):
        # Player must take at least 1, less than MAX_CHIPS, and cannot take more than whats left.
        return list(range(1, min(MAX_CHIPS + 1, self.chips + 1)))

    def getResults(self):
        # If there are no chips left, the other player wins.
        if self.chips == 0:
            return 3 - self.player
        return 0
    def __repr__(self):
        return "Player {0}'s turn: there are {1} chips.".format(self.player, self.chips)

class Node:
    def __init__(self, state: NimState, parent = None, move = None):
        self.state = state
        self.move = move  # the move taken to reach this node
        self.parent = parent  # If node is root, then parent is None
        self.children = []  # Nodes that have been simulated
        self.possibleMoves = self.state.getMoves()  # Moves not yet chosen
        self.wins = defaultdict(int)
        self.visits = 1

    def addChild(self, m):
        nextState = self.state.clone()
        nextState.doMove(m)
        nextNode = Node(nextState, self, m)
        self.children.append(nextNode)
        self.possibleMoves.remove(m)
        return nextNode

    def isLeaf(self):
        # If both lists are empty, then node is a leaf node
        return not self.children and not self.possibleMoves

    def fullyExpanded(self):
        return not self.possibleMoves

    def update(self, value):
        self.wins[value] += 1
        self.visits += 1

    def UCTSelectChild(self, c_factor = 0.5):
        # c_factor: controls the exploration / exploitation. 0 for pure exploitation
        s = sorted(self.children, key = lambda c: c.wins[self.state.player] / c.visits + c_factor * sqrt(2 * log(self.visits) / c.visits))[-1]
        return s
    def TreeString(self, level):
        s = "\t" * level + str(self) + "\n"
        for c in self.children:
            s += c.TreeString(level + 1)
        return s

    def ChildrenString(self):
        s = ""
        for c in self.children:
            s += str(c) + "\n"
        return s
    def __repr__(self):
        return "[S:" + str(self.state) + " W/V:" + str(self.wins[self.state.player]) + "/" + str(self.visits) + " U:" + str(
            self.possibleMoves) + "]"


def search(state : NimState, trials = 100000):
    root = Node(state)
    for trial in range(trials):
        node = root
        # Selection
        while node.fullyExpanded() and not node.isLeaf():
            node = node.UCTSelectChild()
        state = node.state.clone()

        # Expansion
        if node.possibleMoves:

            m = random.choice(node.possibleMoves)
            node = node.addChild(m) # Add child and move to the new node
            state.doMove(m)

        # Simulation
        while state.getMoves():
            # Do a random walk of possible moves
            state.doMove(random.choice(state.getMoves()))

        # Backpropagation

        while node:
            node.update(state.getResults())
            node = node.parent
    # print(root.TreeString(0))
    # print(root.ChildrenString())
    return sorted(root.children, key = lambda c: c.visits)[-1].move

def play():
    state = NimState(16)

    while state.getMoves():
        # print(state)
        if state.player == 1:
            # move = int(input("Nim Move: ").strip())
            move = search(state, trials=10000)
        else:
            move = search(state, trials=10000)

        state.doMove(move)
        pass
    winner = state.getResults()
    if winner == 1:
        print("Player 1 wins!")
    elif winner == 2:
        print("Player 2 wins!")
    else:
        print("Nobody wins!")
    return winner

if __name__ == '__main__':
    win_stats = defaultdict(int)
    for i in range(100):
        winner = play()
        win_stats[winner] += 1
    print(win_stats)
