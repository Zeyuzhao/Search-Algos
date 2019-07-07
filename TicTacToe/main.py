import numpy as np

class TTTGame():
    def __init__(self):
        self.board = np.zeros([3, 3])

    def checkWinner(self, b):

        # Check Row
        val = self.rowCheck(b)
        if val != 0:
            return val

        # Check Column
        val = self.rowCheck(b.T)
        if val != 0:
            return val

        # Check Diagonals
        val = self.diagCheck(b)
        if val != 0:
            return val

        val = self.diagCheck(np.fliplr(b))
        if val != 0:
            return val
        return 0
    def rowCheck(self, b):
        for r in b:
            if len(set(r)) == 1 and r[0] != 0:
                return r[0]
        return 0

    def diagCheck(self, b):
        diag = []
        for i in range(len(b)):
            diag.append(b[i, i])
        if len(set(diag)) == 1 and diag[0] != 0:
            return diag[0]
        return 0

    # Find coordinates where the elements are 0
    def findMoves(self, board):
        z = np.where(board == 0)
        return list(zip(z[0], z[1]))

    def play(self, player1, player2):
        self.board = np.zeros([3, 3])

        turn = 1
        while self.checkWinner(self.board) == 0 and self.findMoves(self.board):
            # print(self.board)
            if turn == 1:
                m = player1.move(self.board.copy())
                self.board[m[0], m[1]] = 1
            else:
                m = player2.move(self.board.copy())
                self.board[m[0], m[1]] = -1
            turn *= -1
        return self.checkWinner(self.board)

class HumanPlayer():
    def move(self, board):
        print(board)
        print()
        while True:
            m = input("Input move: ").strip().split(" ")
            m = [int(x) for x in m]

            if 0 <= m[0] < 3 and 0 <= m[1] < 3 and board[m[0], m[1]] == 0:
                print("******************************")
                return m
            print("Invalid move, please try again!")
class MinimaxPlayer():
    def __init__(self, player):
        self.g = TTTGame()
        self.depthLimit = 9
        self.player = player
    def minimax(self, board, player, depth):
        # print(depth)
        # print(board)

        # Check if there is a winner
        w = self.g.checkWinner(board)
        if w != 0 or len(self.findMoves(board)) == 0:
            # print("Score " + str(w))
            # print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            return w, None

        # print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        # Execute Heuristic

        # if depth > 9:
        #     return 0, None

        if player == 1:
            win_score = -1
            win_move = self.findMoves(board)[0]
            for m in self.findMoves(board):
                temp_board = board
                temp_board[m[0], m[1]] = player
                s, _ = self.minimax(temp_board, -player, depth + 1)
                if s > win_score:
                    win_score = s
                    win_move = m

                # Undo the move
                temp_board[m[0], m[1]] = 0
            return (win_score, win_move)

        else:
            win_score = 1
            win_move = self.findMoves(board)[0]
            for m in self.findMoves(board):
                temp_board = board
                temp_board[m[0], m[1]] = player
                s, _ = self.minimax(temp_board, -player, depth + 1)
                if s < win_score:
                    win_score = s
                    win_move = m

                # Undo the move
                temp_board[m[0], m[1]] = 0
            return (win_score, win_move)

    # Find coordinates where the elements are 0
    def findMoves(self, board):
        z = np.where(board == 0)
        return list(zip(z[0], z[1]))

    def move(self, board):
        return self.minimax(board, self.player, 0)[1]

if __name__ == '__main__':
    g = TTTGame()

    # b = [[1, 0, 0],
    #      [-1, -1, 1],
    #      [1, 0, -1]]

    winner = g.play(HumanPlayer(), MinimaxPlayer(-1))
    print(g.board)

    if winner == 1:
        print("Winner is player 1!")
    elif winner == -1:
        print("Winner is player 2!")
    else:
        print("You are both losers! TEEHEE!!!")
