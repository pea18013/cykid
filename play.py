from mcts import MCTS
from agent import GobangAI
from game import GobangGame

def print_board(board):
    print('   ', end='')
    for i in range(len(board)):
        print(chr(ord('a') + i), end=' ')
    print()
    for i in range(len(board)):
        print('{:2d}'.format(i + 1), end=' ')
        for j in range(len(board)):
            if board[i][j] == 0:
                print('.', end=' ')
            elif board[i][j] == 1:
                print('X', end=' ')
            elif board[i][j] == 2:
                print('O', end=' ')
        print()

def get_human_action(game):
    while True:
        move = input("Please input your move (e.g. a1): ")
        if len(move) == 2 and move[0] in 'abcdefghijklmno' and move[1] in '123456789':
            col = ord(move[0]) - ord('a')
            row = int(move[1:]) - 1
            if game.board[row][col] == 0:
                return row, col
        print("Invalid move, please try again.")

def play_game(game, ai):
    current_player = 1
    while not game.check_win(1) and not game.check_win(2):
        print_board(game.get_board())
        if current_player == 1:
            row, col = get_human_action(game)
        else:
            print("AI is thinking...")
            action = ai.get_action(game.get_board())
            row, col = action
            print("AI has played {}{}".format(chr(ord('a') + col), row + 1))
        game.place_piece(row, col)
        current_player = 3 - current_player
    print_board(game.get_board())
    if game.check_win(1):
        print("You win!")
    elif game.check_win(2):
        print("AI wins!")
    else:
        print("Draw!")

if __name__ == '__main__':
    game = GobangGame()
    mcts = MCTS(game)
    ai = GobangAI(game, mcts)
    play_game(game, ai)