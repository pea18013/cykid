class GobangGame:
    def __init__(self, board_size=15):
        self.board_size = board_size
        self.board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 1

    def get_board(self):
        return self.board

    def get_current_player(self):
        return self.current_player

    def place_piece(self, row, col):
        if self.board[row][col] != 0:
            return False
        self.board[row][col] = self.current_player
        self.current_player = 3 - self.current_player
        return True

    def remove_piece(self, row, col):
        if self.board[row][col] == 0:
            return False
        self.board[row][col] = 0
        self.current_player = 3 - self.current_player
        return True

    def get_legal_actions(self):
        actions = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 0:
                    actions.append((i, j))
        return actions

    def check_win(self, player):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == player:
                    if self.check_five_in_row(i, j, player):
                        return True
        return False

    def check_five_in_row(self, row, col, player):
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for d in directions:
            count = 1
            for i in range(1, 5):
                r = row + i * d[0]
                c = col + i * d[1]
                if r < 0 or r >= self.board_size or c < 0 or c >= self.board_size:
                    break
                if self.board[r][c] != player:
                    break
                count += 1
            if count == 5:
                return True
        return False